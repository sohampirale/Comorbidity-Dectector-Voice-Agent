import os
from model import CCIComorbiditiesOutput
from CCI_indexes import cci_indexes, cci_mapping


async def get_cci_index(clinical_notes: list[str], conversation_history: list[dict]) -> int:
    try:
        from langchain_cohere import ChatCohere
        from langchain_core.messages import SystemMessage, HumanMessage
    except ImportError:
        print(
            "Error: langchain_cohere or langchain_core not installed. Please install with: pip install langchain-cohere langchain-core"
        )
        return 0

    with open(
        "/home/soham/coding/proj/Comorbidity-Dectector-Voice-Agent/voice_agent/pipecat-quickstart/prompts/agents/cci_expert/AGENT.md",
        "r",
    ) as f:
        system_prompt = f.read()

    llm = ChatCohere(
        model="command-r-plus", cohere_api_key=os.getenv("COHERE_API_KEY")
    ).with_structured_output(CCIComorbiditiesOutput)

    cci_indexes_text = "\n".join(
        [
            f"- {item['variable']}: {item['condition']} ({item['points']} points)"
            for item in cci_indexes
        ]
    )

    human_message = f"""
Clinical Notes: {chr(10).join(clinical_notes)}

Conversation History: {chr(10).join(conversation_history)}

Available CCI Variables:
{cci_indexes_text}

Please analyze the patient information and identify any CCI comorbidities present.
"""

    response = await llm.ainvoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=human_message)]
    )

    identified_variables = list(set(response.identified_cci_comorbidities_variables_list))

    total_cci_index = sum(cci_mapping.get(variable, 0) for variable in identified_variables)

    return total_cci_index
