import os
from model import ElixhausterAgentStructure
from Elixhauser_indexes import elixhauser_indexes
from langchain_cohere import ChatCohere
from langchain_core.messages import SystemMessage, HumanMessage


async def get_elixhauser_result(
    clinical_notes: list[str], conversation_history: list[dict]
) -> dict:


    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    agent_md_path = os.path.join(current_dir, "AGENT.md")

    with open(agent_md_path, "r") as f:
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
