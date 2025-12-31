from pydantic import BaseModel, Field


class CCIComorbiditiesOutput(BaseModel):
    identified_cci_comorbidities_variables_list: list[str] = Field(
        description="List of identified Charlson Comorbidity Index conditions. Use exact variable names: MI, CHF, PVD, CVA, PLEGIA, COPD, DM, DMENDORGAN, RENAL, MILD_LIVER, SEVERE_LIVER, ULCER, CANCER, METASTASES, DEMENTIA, RHEUMATIC, HIV, HBP, SKIN_ULCER, DEPRESSION, WARFARIN"
    )
    reason: str = Field(
        description="In-depth clinical explanation for why those specific conditions were identified based on the patient's medical history, symptoms, and clinical findings"
    )
