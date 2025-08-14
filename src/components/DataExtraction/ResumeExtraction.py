import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_agentchat.agents import AssistantAgent
import json
from time import time
from ...utils.system_prompts import candidate_system_message, education_system_message, project_system_message, personal_project_system_message, experience_system_message, certification_system_message


class DataExtraction:
    def __init__(self, model_name, base_url, api_key):
        self.model_name = model_name
        self.base_url = base_url
        self.candidate_info_summary = None
        self.education_info_summary = None
        self.company_project_info_summary = None
        self.personal_project_info_summary = None
        self.experience_info_summary = None
        self.certifications_info_summary = None


        self.model_client = OpenAIChatCompletionClient(
            model = model_name,
            base_url = base_url,
            api_key = api_key
        )

    async def extract_candidate_info(self):
        agent = AssistantAgent(
            name="CandidateDataExtractor",
            description="An Agent for extracting the candidate information from the resume",
            model_client=self.model_client,
            system_message=candidate_system_message
        )
        self.candidate_info_summary = await agent.run()

    async def extract_education_info(self):
        agent = AssistantAgent(
            name="EducationDataExtractor",
            description="An Agent for extracting the education information from the resume",
            model_client=self.model_client,
            system_message=education_system_message
        )
        self.education_info_summary = await agent.run()

    async def extract_company_projects_info(self):
        agent = AssistantAgent(
            name="CompanyProjectDataExtractor",
            description="An Agent for extracting the company project information from the resume",
            model_client=self.model_client,
            system_message=project_system_message
        )
        self.company_project_info_summary = await agent.run()

    async def extract_personal_projects_info(self):
        agent = AssistantAgent(
            name="PersonalProjectDataExtractor",
            description="An Agent for extracting the personal project information from the resume",
            model_client=self.model_client,
            system_message=personal_project_system_message
        )
        self.personal_project_info_summary = await agent.run()

    async def extract_experience_info(self):
        agent = AssistantAgent(
            name="ExperienceDataExtractor",
            description="An Agent for extracting the experience information from the resume",
            model_client=self.model_client,
            system_message=experience_system_message
        )
        self.experience_info_summary = await agent.run()

    async def extract_certification_info(self):
        agent = AssistantAgent(
            name="CertificationDataExtractor",
            description="An Agent for extracting the experience information from the resume",
            model_client=self.model_client,
            system_message=certification_system_message
        )
        self.certifications_info_summary = await agent.run()



if __name__ == "__main__":
    load_dotenv()
    api_key_gemini = os.getenv('GOOGLE_API_KEY')
    model_name = "gemini-2.5-flash",
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
    data_extraction = DataExtraction(model_name = model_name, base_url=base_url, api_key=api_key_gemini)
