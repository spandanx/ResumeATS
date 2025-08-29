from typing import List, Optional
from pydantic import Field, BaseModel

class Candidate(BaseModel):
    name: str = Field(description="Name of the person, return 'NOT FOUND' if not found")
    contact_number: Optional[str] = Field(description="Contact number of the person, return 'NOT FOUND' if not found")
    email_id: str = Field(description="Email address of the person, return 'NOT FOUND' if not found")
    linkedin_profile_link: str = Field(description="Link to the LinkedIn profile of the person, return 'NOT FOUND' if not found")
    github_profile_link: str = Field(description="Link to the Github profile of the person, return 'NOT FOUND' if not found")
    other_information: str = Field(description="Other information related to the candidate")

class Education(BaseModel):
    institution_name: str = Field(description="Name of the institution/college/school, return 'NOT FOUND' if not found")
    marks: str = Field(description="Marks/CGPA received from the institution/college/school, return 'NOT FOUND' if not found")
    location: str = Field(description="Location of the institution/college/school, return 'NOT FOUND' if not found")
    duration: str = Field(description="Duration or timeline of the education, return 'NOT FOUND' if not found")
    other_information: str = Field(description="Other educational information")

class Project(BaseModel):
    project_name: str = Field(description="Name of the project, return 'NOT FOUND' if not found")
    project_description: str = Field(description="Short description of the project, return 'NOT FOUND' if not found")
    complete_description: List[str] = Field(description="Complete descriptions of the project, return empty list is not found")
    technology: List[str] = Field(description="Technologies, tools or softwares used in the project, return empty list is not found")
    duration: str = Field(description="Duration or timeline of the project, return 'NOT FOUND' if not found")

class Experience(BaseModel):
    company_name: str = Field(description="Name of the company the person worked with, return 'NOT FOUND' if not found")
    designation: str = Field(description="Designation name for the person in the company, return 'NOT FOUND' if not found")
    contributions: List[str] = Field(description="contributions or works done in the project, return empty list is not found")
    technology: List[str] = Field(description="Technologies or tools or softwares used in the company, return empty list is not found")
    duration: str = Field(description="Duration or timeline for the experience in the company, return 'NOT FOUND' if not found")

class Certification(BaseModel):
    certification_name: str = Field(description="Name of the certification, return 'NOT FOUND' is not found")
    certification_authority: str = Field(description="Name of the certification authority or company, return 'NOT FOUND' is not found")
    duration: str = Field(description="Duration or timeline of the certification, return 'NOT FOUND' if not found")

class OtherCategory(BaseModel):
    category_name: str = Field(description="Name of the category")
    summary: str = Field(description="Summary of the content present in the category")

class Resume(BaseModel):
    candidate_information: Candidate = Field(description="Information related to the candidate")
    education: List[Education] = Field(description="list of the educational information, return empty list if not found")
    personal_projects: List[Project] = Field(description="list of the personal projects mentioned in the resume is available. Consider only personal projects and do not consider company projects, return empty list if not found")
    skills: List[str] = Field(description="Skills of the person")
    experience: List[Experience] = Field(description="list of the company experiences available in the resume, return empty list if not found")
    achievements: List[str] = Field(description="Achievements made or reward received during working in companies, return empty list if not found")
    certifications: List[Certification] = Field(description="List of the certifications, return empty list if not found")
    others: List[OtherCategory] = Field(description="List of components that does not lie in any already defined category")