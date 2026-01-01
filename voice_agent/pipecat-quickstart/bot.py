#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Pipecat Quickstart Example.

The example runs a simple voice AI bot that you can connect to using your
browser and speak with it. You can also deploy this bot to Pipecat Cloud.

Required AI services:
- Deepgram (Speech-to-Text)
- OpenAI (LLM)
- Cartesia (Text-to-Speech)

Run the bot using::

    uv run bot.py
"""

import os

from dotenv import load_dotenv
from loguru import logger

print("🚀 Starting Pipecat bot...")
print("⏳ Loading models and imports (20 seconds, first run only)\n")

logger.info("Loading Local Smart Turn Analyzer V3...")
from pipecat.audio.turn.smart_turn.local_smart_turn_v3 import LocalSmartTurnAnalyzerV3

logger.info("✅ Local Smart Turn Analyzer V3 loaded")
logger.info("Loading Silero VAD model...")
from pipecat.audio.vad.silero import SileroVADAnalyzer

logger.info("✅ Silero VAD model loaded")

from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.frames.frames import LLMRunFrame

logger.info("Loading pipeline components...")
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.transports.daily.transport import DailyParams

logger.info("✅ All components loaded successfully!")

#
from pipecat.processors.frameworks.strands_agents import StrandsAgentsProcessor
from strands import Agent,tool
from strands.models.litellm import LiteLLMModel
#from strands_tools import calculator 
from helpers.read_md import read_md
from pipecat.services.deepgram.tts import DeepgramTTSService
from deepgram import LiveOptions
from pipecat.transcriptions.language import Language
import asyncio
from helpers.analyze_comorbidities import analyze_comorbidities


load_dotenv(override=True)



async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
    logger.info(f"Starting bot")

    notes:list[str]=[]

    @tool
    def add_note(note:str):
        """Tool to add notes to review later for Comorbidity identification (with CCI, Elixhauser,ICD_10) after end of call
        Args:
        note: str - The note to add to the notes list
        """
        notes.append(note)
        return "Note added successfully"

    @tool
    async def end_call():
        """Tool to end the call"""
        print(f"Notes: {notes}")
        asyncio.create_task(asyncio.to_thread(await analyze_comorbidities(notes,context.messages)))
        return "Call ended successfully"


    live_options = LiveOptions(
        model="nova-3",
        language=Language.EN_US,  
        interim_results=True,
        smart_format=True,
    )

    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"), live_options=live_options)

    # tts = CartesiaTTSService(
    #     api_key=os.getenv("CARTESIA_API_KEY"),
    #     voice_id="71a7ad14-091c-4e8e-a314-022ece01c121",  # British Reading Lady
    # )


    tts = DeepgramTTSService(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
        # voice_id="aura-asteria-en",  
        voice_id="aura-2-andromeda-en", 
    )

    #llm 
    model = LiteLLMModel(
        client_args={
            "api_key":os.getenv('OPENROUTER_API_KEY'),
        },
        model_id="openrouter/openai/gpt-4o-mini",
        # model_id="openrouter/google/gemini-2.0-flash-lite-001",
        # model_id="openrouter/google/gemini-2.0-flash-exp:free",
        # model_id="openrouter/google/gemini-2.0-flash-001",
        # model_id="openrouter/google/gemini-2.5-pro",
        params={
            'temperature':0.5,
            "max_tokens":1000
        },
    )

    # agent_prompt = read_md("prompts/agents/patient_onboard_agent/CLAUDE.md")
    agent_prompt = read_md("prompts/agents/patient_onboard_agent/AGENT.md")


    agent = Agent(
        model=model,
        tools=[add_note, end_call],
        system_prompt=agent_prompt
    )

    llm = StrandsAgentsProcessor(agent=agent)

    messages = [
        {
            "role": "system",
            "content": "Start by getting consent from the user and then proceed with the conversation",
        },
    ]

    context = LLMContext(messages)
    context_aggregator = LLMContextAggregatorPair(context)

    rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

    pipeline = Pipeline(
        [
            transport.input(),  # Transport user input
            rtvi,  # RTVI processor
            stt,
            context_aggregator.user(),  # User responses
            llm,  # LLM
            tts,  # TTS
            transport.output(),  # Transport bot output
            context_aggregator.assistant(),  # Assistant spoken responses
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
        observers=[RTVIObserver(rtvi)],
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info(f"Client connected")
        # Kick off the conversation.
        messages.append({"role": "system", "content": "Say hello and briefly introduce yourself."})
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info(f"Client disconnected")
        print(f"Notes: {notes}")
        await task.cancel()

    runner = PipelineRunner(handle_sigint=runner_args.handle_sigint)

    await runner.run(task)


async def bot(runner_args: RunnerArguments):
    """Main bot entry point for the bot starter."""

    transport_params = {
        "daily": lambda: DailyParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
            turn_analyzer=LocalSmartTurnAnalyzerV3(),
        ),
        "webrtc": lambda: TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
            turn_analyzer=LocalSmartTurnAnalyzerV3(),
        ),
    }

    transport = await create_transport(runner_args, transport_params)

    await run_bot(transport, runner_args)


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()
