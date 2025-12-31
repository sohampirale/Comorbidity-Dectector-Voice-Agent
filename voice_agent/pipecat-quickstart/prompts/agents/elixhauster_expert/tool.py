import os
from model import ElixhausterAgentStructure
from Elixhauser_indexes import elixhauser_indexes


async def get_elixhauser_result(
    clinical_notes: list[str], conversation_history: list[dict]
) -> dict:
    try:
        from langchain_cohere import ChatCohere
        from langchain_core.messages import SystemMessage, HumanMessage
    except ImportError:
        print(
            "Error: langchain_cohere or langchain_core not installed. Please install with: pip install langchain-cohere langchain-core"
        )
        return elixhauser_indexes

    with open(
        "/home/soham/coding/proj/Comorbidity-Dectector-Voice-Agent/voice_agent/pipecat-quickstart/prompts/agents/elixhauster_expert/AGENT.md",
        "r",
    ) as f:
        system_prompt = f.read()

    llm = ChatCohere(
        model="command-r-plus", cohere_api_key=os.getenv("COHERE_API_KEY")
    ).with_structured_output(ElixhausterAgentStructure)

    elixhauser_indexes_text = "\n".join(
        [
            f"- {condition}: {('Present' if value else 'Absent')}"
            for condition, value in elixhauser_indexes.items()
        ]
    )

    # Format conversation history for display
    conversation_text = "\n".join(
        [f"Turn {i + 1}: {conv.get('text', 'N/A')}" for i, conv in enumerate(conversation_history)]
    )

    human_message = f"""
Clinical Notes: {chr(10).join(clinical_notes)}

Conversation History: {chr(10).join(conversation_text)}

Available Elixhauser Comorbidities:
{elixhauser_indexes_text}

Please analyze the patient information and identify any Elixhauser comorbidities present.
"""

    response = await llm.ainvoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=human_message)]
    )

    # Create a copy of elixhauser_indexes to modify
    result_indexes = elixhauser_indexes.copy()

    # Mark identified comorbidities as True
    identified_comorbidities = list(set(response.identified_elixhauser_comorbidities_list))

    for comorbidity in identified_comorbidities:
        if comorbidity in result_indexes:
            result_indexes[comorbidity] = True

    return result_indexes
