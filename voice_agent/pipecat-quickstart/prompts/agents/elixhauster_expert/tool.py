import os
from prompts.agents.elixhauster_expert.model import ElixhausterAgentStructure
from prompts.agents.elixhauster_expert.Elixhauser_indexes import elixhauser_indexes

# from langchain_cohere import ChatCohere
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI


async def get_elixhauser_result(
    clinical_notes: list[str], conversation_history: list[dict]
) -> dict:
    print("inside get_elixhauser_result")
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        agent_md_path = os.path.join(current_dir, "AGENT.md")

        with open(agent_md_path, "r") as f:
            system_prompt = f.read()

        # llm = ChatCohere(
        #     model="command-r-plus-08-2024", cohere_api_key=os.getenv("COHERE_API_KEY")
        # ).with_structured_output(ElixhauserAgentStructure)

        llm = ChatOpenAI(
            model="openai/gpt-4o-mini",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        ).with_structured_output(ElixhausterAgentStructure)

        elixhauser_indexes_text = "\n".join(
            [
                f"- {condition}: {('Present' if value else 'Absent')}"
                for condition, value in elixhauser_indexes.items()
            ]
        )

        # Format conversation history for display
        conversation_text = "\n".join(
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in conversation_history
            if isinstance(msg, dict)
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

        print(f"response from get_elixhauser_result: {response}")

        # Create a copy of elixhauser_indexes to modify
        result_indexes = elixhauser_indexes.copy()

        # Mark identified comorbidities as True
        identified_comorbidities = list(set(response.identified_elixhauser_comorbidities_list))

        for comorbidity in identified_comorbidities:
            if comorbidity in result_indexes:
                result_indexes[comorbidity] = True

        return result_indexes
    except Exception as e:
        print(f"Error in get_elixhauser_result: {e}")
        return elixhauser_indexes
