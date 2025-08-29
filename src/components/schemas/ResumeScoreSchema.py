from typing import List, Optional
from pydantic import Field, BaseModel

class Score(BaseModel):
    category: str = Field(description="Name of the category for the similarity calculation, keep the name in lower snake case, example - name_of_the_category")
    score: float = Field(description="Score of the component")
    justification: str = Field(description="Detailed justification behind the calculated score for the component")
    improvement_suggestions: List[str] = Field(description="Detailed suggestions, or improvements from resume perspective that can be taken to improve the score")

class ResumeScore(BaseModel):
    scoring_sections: List[Score] = Field(description="Score for different components like candidate information, education, experience etc")
    # candidate_information: Score = Field(description="Score for candidate information")
    # education: Score = Field(description="Score on education information")
    # company_projects: Score = Field(description="Score on company project information")
    # personal_projects: Score = Field(description="Score on personal project information")
    # skills: Score = Field(description="Score on skill information")
    # experience: Score = Field(description="Score on experience information")
    # achievements: Score = Field(description="Score on achievement information")
    # certifications: Score = Field(description="Score on certification information")