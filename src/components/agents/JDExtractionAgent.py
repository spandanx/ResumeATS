from typing import Sequence

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio
import sys
# sys.path.append("..")
# sys.path.append('components')
# sys.path.append('src.components')
 # or sys.path.insert(0, 'path/to/your/folder'))

from src.components.schemas.JobDescriptionSchema import JobDescription
from src.components.prompts.system_prompts import job_description_system_prompt
from src.components.prompts.user_prompts import job_description_user_prompt

from dotenv import load_dotenv
import os

load_dotenv()

class JDExtractionAgent:

    def __init__(self):

        self.model_resume_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv('OPEN_API_KEY'),
            response_format=JobDescription,
            max_retries=3,  # Retry up to 3 times on failures
            timeout=20  # 20-second timeout per attempt
        )

        self.complete_jd_extraction_agent = AssistantAgent(
            name="JDExtractionAgent",
            description="An Agent for extracting job description",
            system_message=job_description_system_prompt,
            model_client=self.model_resume_client
        )

    async def extract_job_description(self, task):
        prompt = job_description_user_prompt.format(**task)
        response = await self.complete_jd_extraction_agent.run(task=prompt)
        # print(response)
        return response


if __name__ == "__main__":
    resumeHandler = JDExtractionAgent()
    # response = resumeHandler.process_resume()

    # asyncio.run(resumeHandler.extract_resume(task))
