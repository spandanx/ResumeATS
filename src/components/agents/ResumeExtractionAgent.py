from typing import Sequence

from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent, UserProxyAgent
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console

import asyncio
import sys
# sys.path.append("..")
# sys.path.append('components')
 # or sys.path.insert(0, 'path/to/your/folder'))


from src.components.schemas.ResumeSchema import Resume, Candidate
from src.components.prompts.system_prompts import complete_resume_extraction_system_prompt
from src.components.prompts.user_prompts import complete_resume_extraction_user_prompt

# from components.schemas.ResumeSchema import Resume, Candidate
# from components.prompts.system_prompts import complete_resume_extraction_system_prompt
# from components.prompts.user_prompts import complete_resume_extraction_user_prompt

from dotenv import load_dotenv
import os

load_dotenv()

class ResumeDataExtractingAgent:

    def __init__(self):

        self.model_resume_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv('OPEN_API_KEY'),
            response_format=Resume,
            max_retries=3,  # Retry up to 3 times on failures
            timeout=20  # 20-second timeout per attempt
        )

        self.complete_resume_extraction_agent = AssistantAgent(
            name="ResumeCompleteDataExtractingAgent",
            description="An Agent for extracting complete information from raw text",
            system_message=complete_resume_extraction_system_prompt,
            model_client=self.model_resume_client
        )

    async def extract_resume(self, task):
        prompt = complete_resume_extraction_user_prompt.format(**task)
        response = await self.complete_resume_extraction_agent.run(task=prompt)
        # print(response)
        return response


if __name__ == "__main__":
    resumeHandler = ResumeDataExtractingAgent()
    # response = resumeHandler.process_resume()
