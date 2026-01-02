from prompts.agents.cci_expert.tool import get_cci_index
from prompts.agents.elixhauster_expert.tool import get_elixhauser_result
from prompts.agents.icd_10_codes_expert.tool import analyze_icd_codes


async def analyze_comorbidities(clinical_notes: list[str], conversation_history: list[dict]):
    """
    Analyze comorbidities using both CCI and Elixhauser indexes.

    Args:
        clinical_notes: List of clinical notes strings
        conversation_history: List of conversation history dictionaries

    Returns:
        tuple: (cci_index, elixhauser_dict)
    """
    print("inside analyze_comorbidities")
    if get_cci_index is None:
        print("Warning: CCI tool not available, returning 0")
        cci_index = 0
    else:
        cci_index = await get_cci_index(clinical_notes, conversation_history)

    if get_elixhauser_result is None:
        print("Warning: Elixhauser tool not available, returning empty dict")
        elixhauser_dict = {}
    else:
        elixhauser_dict = await get_elixhauser_result(clinical_notes, conversation_history)

    if analyze_icd_codes is None:
        print("Warning: analyze_icd_codes tool not available, returning {}")
        icd_codes_data = {}
    else:
        icd_codes_data = await analyze_icd_codes(clinical_notes, conversation_history)

    print(f"CCI Index: {cci_index}")
    print(f"Elixhauser Dict: {elixhauser_dict}")
    print(f"icd_codes_data : {icd_codes_data}")

    # Handle empty icd_codes_data to avoid KeyError
    if icd_codes_data and "icd_codes" in icd_codes_data:
        icd_codes = icd_codes_data["icd_codes"]
        icd_codes_report = icd_codes_data.get("icd_codes_report", "")
    else:
        icd_codes = []
        icd_codes_report = ""
    
    return cci_index, elixhauser_dict
