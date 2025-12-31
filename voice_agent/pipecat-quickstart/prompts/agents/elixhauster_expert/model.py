from pydantic import BaseModel, Field
from typing import List


class ElixhausterAgentStructure(BaseModel):
    identified_elixhauser_comorbidities_list: List[str] = Field(
        description="""List of identified Elixhauser comorbidities from the following options: 
        congestive_heart_failure, cardiac_arrhythmia,pulmonary_circulation_disorder, peripheral_vascular_disease,hypertension_uncomplicated, hypertension_complicated, paralysis,other_neurological_disorders, chronic_pulmonary_disease, diabetes_uncomplicated, diabetes_complicated, hypothyroidism, renal_failure, liver_disease, peptic_ulcer_disease, aids_hiv, lymphoma, metastatic_cancer, solid_tumor_without_metastasis, rheumatoid_arthritis_collagen_vascular, coagulopathy, obesity, weight_loss, fluid_electrolyte_disorders, blood_loss_anemia, deficiency_anemia, alcohol_abuse, drug_abuse, psychoses, depression
        """
    )
    reason: str = Field(
        description="In-depth clinical explanation on why those specific comorbidities were chosen "
        "based on the patient's medical history, symptoms, and clinical presentation. "
        "Include evidence-based reasoning and clinical justification for each identified condition."
    )
