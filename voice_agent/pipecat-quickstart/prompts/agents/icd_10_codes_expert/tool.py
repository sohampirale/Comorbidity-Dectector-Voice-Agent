import os
from prompts.agents.icd_10_codes_expert.lookup_icd import lookup_icd
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

async def analyze_icd_codes(clinical_notes: list[str], conversation_history: list[dict]):
    icd_codes = []

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    agent_md_path = os.path.join(current_dir, "AGENT.md")

    with open(agent_md_path, "r") as f:
        agent_prompt = f.read()

    @tool
    def add_icd(ICD_10_CODE: str, long_description: str, clinical_reason: str):
        """
        Adds an ICD-10 code to the patient's diagnosis list after validation.

        This function validates and stores ICD-10 codes that have been identified
        from clinical notes. Each code must be accompanied by its official description
        and a clinical justification for why it applies to the specific patient.

        Args:
            ICD_10_CODE (str): The exact ICD-10 code obtained from the lookup_icd tool.
                              Must be a valid, non-empty code string.
            long_description (str): The complete official LONG_DESCRIPTION of the ICD-10 code
                                   as returned by the lookup_icd tool. Must match exactly.
            clinical_reason (str): A clear, patient-specific explanation of why this
                                 ICD-10 code was chosen based on the clinical evidence.
                                 Must provide medical justification for the diagnosis.

        Returns:
            str: Success message if all parameters are valid, or an error message
                 indicating which parameter is empty or invalid.

        Note:
            - All three parameters are mandatory and undergo validation
            - This is a tool function intended for AI agent use in clinical analysis
        """

        # Validate all parameters
        if not ICD_10_CODE or not ICD_10_CODE.strip():
            return "ICD_10_CODE is empty, cannot be empty"
        if not long_description or not long_description.strip():
            return "long_description is empty, cannot be empty"
        if not clinical_reason or not clinical_reason.strip():
            return "clinical_reason is empty, cannot be empty"

        icd_codes.append(
            {
                "ICD_10_CODE": ICD_10_CODE,
                "long_description": long_description,
                "clinical_reason": clinical_reason,
            }
        )

        return "Given ICD_10_CODE added successfully to the list"

    llm = ChatOpenAI(
        model="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    ).bind_tools([lookup_icd, add_icd])

    conversation_text = "\n".join(
        f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
        for msg in conversation_history
        if isinstance(msg, dict)
    )

    human_message = f"""
    Clinical Notes: {chr(10).join(clinical_notes)}

    Conversation History: {conversation_text}

    Please analyze the patient information and identify relevant ICD-10 codes using the lookup_icd tool, then add them to the diagnosis list using the add_icd tool. Provide a clear explanation of what ICD codes were chosen and what they depict for this specific patient.
    """

    response = await llm.ainvoke(
        [SystemMessage(content=agent_prompt), HumanMessage(content=human_message)]
    )

    print(f"response from analyze_icd_codes: {response}")

    return {'icd_codes':icd_codes,'icd_codes_report':response.content}
