from prompts.agents.cci_expert.tool import get_cci_index
from prompts.agents.elixhauster_expert.tool import get_elixhauser_result

async def analyze_comorbidities(clinical_notes: list[str], conversation_history: list[dict]):
    """
    Analyze comorbidities using both CCI and Elixhauser indexes.

    Args:
        clinical_notes: List of clinical notes strings
        conversation_history: List of conversation history dictionaries

    Returns:
        tuple: (cci_index, elixhauser_dict)
    """
    # Check if tools are available
    print('inside analyze_comorbidities')
    if get_cci_index is None:
        print("Warning: CCI tool not available, returning 0")
        cci_index = 0
    else:
        # Generate CCI index
        cci_index = await get_cci_index(clinical_notes, conversation_history)

    if get_elixhauser_result is None:
        print("Warning: Elixhauser tool not available, returning empty dict")
        elixhauser_dict = {}
    else:
        # Generate Elixhauser dict
        elixhauser_dict = await get_elixhauser_result(clinical_notes, conversation_history)

    # Print both results
    print(f"CCI Index: {cci_index}")
    print(f"Elixhauser Dict: {elixhauser_dict}")

    return cci_index, elixhauser_dict
