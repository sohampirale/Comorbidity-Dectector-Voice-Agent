from datetime import datetime
from typing import Optional, Dict, Any, Literal, TYPE_CHECKING
from beanie import Document, Indexed, Link
from pydantic import Field, ConfigDict

if TYPE_CHECKING:
    from models import Patient


class Patient(Document):
    """
    Patient collection model
    """

    name: Optional[str] = Field(None, description="Patient name")
    gender: Optional[Literal["male", "female", "other"]] = Field(None, description="Patient gender")
    birthDate: Optional[datetime] = Field(None, description="Patient birth date")

    model_config = ConfigDict(
        populate_by_name=True, str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    class Settings:
        name = "patients"


class Condition(Document):
    """
    Condition collection model
    """

    subject: Link[Patient] = Field(..., description="Reference to patient document")
    clinical_status: Literal[
        "active", "recurrence", "relapse", "inactive", "remission", "resolved"
    ] = Field(..., description="Clinical status of the condition")
    code: str = Field(..., description="ICD_10 code")
    note: Optional[str] = Field(None, description="Optional notes about the condition")
    description: Optional[str] = Field(None,description="Long description of the ICD_10 code")
    model_config = ConfigDict(
        populate_by_name=True, str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    class Settings:
        name = "conditions"


class Observation(Document):
    """
    Observation collection model
    """

    subject: Link[Patient] = Field(..., description="Reference to patient document")
    effectiveDateTime: datetime = Field(..., description="Date and time when observation was made")
    code: str = Field(..., description="What this observation is about")

    valueInteger: Optional[int] = Field(None, description="Calculated CCI index")
    component: Optional[Dict[str, Any]] = Field(None, description="Alixhauster Dictionary")

    model_config = ConfigDict(
        populate_by_name=True, str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    class Settings:
        name = "observations"
