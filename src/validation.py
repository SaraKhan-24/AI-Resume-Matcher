from pydantic import BaseModel
from pydantic import Field
from typing import Optional, Literal

DATE_PATTERN = r"^\d{4}(-\d{2}(-\d{2})?)?$"
class ExperienceEntry(BaseModel):
    title: str
    company: str
    job_type: Optional[Literal["Full-Time","Part-Time","Internship"]] = None
    start_date: Optional[str] = Field(default = None, pattern = DATE_PATTERN)
    end_date: Optional[str] = Field(default = None, pattern = DATE_PATTERN)

class EducationEntry(BaseModel):
    institution: str
    field_of_study: str
    gpa: Optional[float] = None
    start_date: Optional[str] = Field(default = None, pattern = DATE_PATTERN)
    end_date: Optional[str] = Field(default = None, pattern = DATE_PATTERN)

class Candidate(BaseModel):
    name: str
    #TODO: Do not allow empty strings for the name, resumes without names are useless.
    role: str = ""
    description:str = ""
    skills:list[str] = []
    experience:list[ExperienceEntry] = []
    education:list[EducationEntry] = []
