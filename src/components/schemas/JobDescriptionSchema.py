from typing import List, Optional
from pydantic import Field, BaseModel

class JobDescription(BaseModel):
    responsibilities: List[str] = Field(description="Responsibilities of the role")
    skills: List[str] = Field(description="Skill set needed for the role, return empty list if not found")
    qualifications: Optional[List[str]] = Field(description="list of the qualifications found from the job description, return empty list if not found")
    experience: Optional[List[str]] = Field(description="list of the required experiences available in the job description, return empty list if not found")
    salary: Optional[str] = Field(description="Salary expectations if present in the job description, return 'Not Mentioned' if not found'")
    certifications: Optional[List[str]] = Field(description="List of the certifications expected for this role")