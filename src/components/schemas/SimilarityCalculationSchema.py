from typing import List, Optional
from pydantic import Field, BaseModel

class Similarity(BaseModel):
    category: str = Field(description="Name of the category for the similarity calculation, , keep the name in lower snake case, example - name_of_the_category")
    similarity_score: float = Field(description="Similarity score for the component between job description and resume, The score should be between 0 to 10")
    justification: str = Field(description="Detailed justification behind the calculated similarity score for the component")
    suggestions: Optional[List[str]] = Field(description="list of suggestions to improve the similarity score")

class SimilarityScoreSchema(BaseModel):
    scoring_sections: List[Similarity] = Field(description="Similarity score information between different components")