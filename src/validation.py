from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date

class ExperienceEntry(BaseModel):
    title: str
    company: str
    job_type: Optional[Literal["Full-Time","Part-Time","Internship"]] = None
    start_date: date
    end_date:Optional[date] = None

class EducationEntry(BaseModel):
    institution: str
    field_of_study: str
    gpa: Optional[float] = None
    start_date: date
    end_date:Optional[date] = None

class Candidate(BaseModel):
    name:str
    description:str=""
    skills:list[str]=[]
    experience:list[ExperienceEntry]=[]
    education:list[EducationEntry]=[]
