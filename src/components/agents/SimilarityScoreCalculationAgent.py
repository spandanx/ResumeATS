from typing import Sequence

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio
import sys

from src.components.schemas.SimilarityCalculationSchema import SimilarityScoreSchema
from src.components.prompts.system_prompts import similarity_score_system_prompt
from src.components.prompts.user_prompts import similarity_score_user_prompt

# from components.schemas.SimilarityCalculationSchema import SimilarityScoreSchema
# from components.prompts.system_prompts import similarity_score_system_prompt
# from components.prompts.user_prompts import similarity_score_user_prompt

from dotenv import load_dotenv
import os

load_dotenv()

class SimilarityScoreCalculationAgent:

    def __init__(self):

        self.model_resume_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv('OPEN_API_KEY'),
            response_format=SimilarityScoreSchema,
            max_retries=3,  # Retry up to 3 times on failures
            timeout=20  # 20-second timeout per attempt
        )

        self.complete_resume_extraction_agent = AssistantAgent(
            name="ResumeScoringAgent",
            description="An Agent for extracting complete information from raw text",
            system_message=similarity_score_system_prompt,
            model_client=self.model_resume_client
        )

    async def calculate_similarity_score(self, task):
        prompt = similarity_score_user_prompt.format(**task)
        response = await self.complete_resume_extraction_agent.run(task=prompt)
        # print(response)
        return response


if __name__ == "__main__":
    similarityScoreCalculationAgent = SimilarityScoreCalculationAgent()
    # response = resumeHandler.process_resume()

    # asyncio.run(resumeHandler.extract_resume(task))
