import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_agentchat.agents import AssistantAgent
import sys
sys.path.append("..")
from model.ResumeModel import Candidate, Education, Project, Experience, Certification
from utils.system_prompts import (candidate_system_message, education_system_message, company_project_system_message,
                                  personal_project_system_message, experience_system_message, certification_system_message)

class ComponentWiseDataExtraction:
    def __init__(self, api_key):

        self.candidate_model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
            response_format=Candidate
        )

        self.education_model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
            response_format=Education
        )

        self.project_model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
            response_format=Project
        )

        self.experience_model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
            response_format=Experience
        )

        self.experience_model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
            response_format=Experience
        )

        self.certification_model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
            response_format=Certification
        )

        self.candidateDataExtractorAgent = AssistantAgent(
            name="CandidateDataExtractor",
            description="An Agent for extracting the candidate information from the resume",
            model_client=self.candidate_model_client,
            system_message=candidate_system_message
        )

        self.educationDataExtractorAgent = AssistantAgent(
            name="EducationDataExtractor",
            description="An Agent for extracting the education information from the resume",
            model_client=self.education_model_client,
            system_message=education_system_message
        )

        self.companyProjectDataExtractorAgent = AssistantAgent(
            name="CompanyProjectDataExtractor",
            description="An Agent for extracting the company project information from the resume",
            model_client=self.project_model_client,
            system_message=company_project_system_message
        )

        self.personalProjectDataExtractorAgent = AssistantAgent(
            name="PersonalProjectDataExtractor",
            description="An Agent for extracting the personal project information from the resume",
            model_client=self.project_model_client,
            system_message=personal_project_system_message
        )

        self.experienceDataExtractorAgent = AssistantAgent(
            name="ExperienceDataExtractor",
            description="An Agent for extracting the experience information from the resume",
            model_client=self.experience_model_client,
            system_message=experience_system_message
        )

        self.certificationDataExtractorAgent = AssistantAgent(
            name="CertificationDataExtractor",
            description="An Agent for extracting the certification information from the resume, return an empty sting if not found",
            model_client=self.certification_model_client,
            system_message=certification_system_message
        )