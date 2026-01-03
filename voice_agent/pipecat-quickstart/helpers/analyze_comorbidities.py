from prompts.agents.cci_expert.tool import get_cci_index
from prompts.agents.elixhauster_expert.tool import get_elixhauser_result
from prompts.agents.icd_10_codes_expert.tool import analyze_icd_codes
from prompts.agents.db_expert.models import Patient,Condition,Observation
from prompts.agents.db_expert.database import get_database,ensure_db_initialized
from datetime import datetime



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
    await ensure_db_initialized()

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

    if icd_codes_data and "icd_codes" in icd_codes_data:
        icd_codes = icd_codes_data["icd_codes"]
        icd_codes_report = icd_codes_data.get("icd_codes_report", "")
    else:
        icd_codes = []
        icd_codes_report = ""

    
    subject = None
    try:
        patient = Patient()
        result = await patient.save()
        print(f'patient : {result}')
        subject = result.id
    except Exception as e:
        subject = '122121'
        print(f'Error creating patient : {e}')

    try:
        for icd_code_dict in icd_codes:
            ICD_10_CODE = icd_code_dict['ICD_10_CODE']
            description = icd_code_dict['long_description']
            note= icd_code_dict['clinical_reason']
            condition = Condition(code=ICD_10_CODE,clinical_status='active',note=note,description=description,subject=subject)
            condition=await condition.save()
            print(f'Condition : {condition}')
    except Exception as e:
        print(f'Error creating conditions : {e}')
    
    component = elixhauser_dict
    valueInteger = cci_index
    effectiveDateTime = datetime.now()

    try:
        cci_observation = Observation(subject=subject,valueInteger=valueInteger,code='CCI Index',effectiveDateTime=effectiveDateTime)
        elixhauster_observation = Observation(subject=subject,component=component,code='Elixhauster dict',effectiveDateTime=effectiveDateTime)

        cci_observation=await cci_observation.save()
        elixhauster_observation=await elixhauster_observation.save()
        print(f'cci_observation : {cci_observation}')
        print(f'elixhauster_observation : {elixhauster_observation}')
    except Exception as e:
        print(f'Error creating observations : {e}')
    
    return cci_index, elixhauser_dict
