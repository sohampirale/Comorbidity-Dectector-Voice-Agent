import os
from model import CCIComorbiditiesOutput
from CCI_indexes import cci_indexes, cci_mapping
from langchain_cohere import ChatCohere
from langchain_core.messages import SystemMessage, HumanMessage


async def get_cci_index(clinical_notes: list[str], conversation_history: list[dict]) -> int:
  

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    agent_md_path = os.path.join(current_dir, "AGENT.md")

    with open(agent_md_path, "r") as f:
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
