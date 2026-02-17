import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_agentchat.agents import AssistantAgent
from concurrent.futures import ThreadPoolExecutor

from time import time
import sys
sys.path.append("..")

from model.ResumeModel import Resume

task = """
"""

# complete_resume_system_message = """
# You are a resume analyzer.
#
# An ideal resume can contain the below components:
#
# ** A. Candidate information **
#     1. Name: Name of the person
#     2. Contact number: Contact number of the person
#     3. Email address: Email address of the person
#     4. LinkedIn ID: link to the LinkedIn profile of the person
#     5. GitHub ID: link to the Github profile of the person
# ** B. Education information **
#     1. Institution name: Name of the institution/college/school
#     2. Marks: Marks/CGPA received from the institution/college/school
#     3. Location: Location of the institution/college/school
#     4. Duration: Duration or timeline of the education
# ** C. Company Project information **
#     1. Project name: Name of the project
#     2. Project description: Short description of the project
#     3. Complete description: Complete descriptions of the project
#     4. Technology: Duration or timeline of the education
#     5. Duration: Duration or timeline of the project
# ** D. Personal Project information **
#     1. Project name: Name of the project
#     2. Project description: Short description of the project
#     3. Complete description: Complete descriptions of the project
#     4. Technology: Duration or timeline of the education
#     5. Duration: Duration or timeline of the project
# ** E. Experience information **
#     1. Company name: Name of the company the person worked with
#     2. Designation: Designation name for the person in the company
#     3. Contributions: Contributions or works done in the project
#     4. Technology: Technologies, tools or softwares used in the company
#     5. Duration: Duration or timeline for the experience in the company
# ** F. Certification information **
#     1. Certification name: Name of the certification
#     2. Certification Authority: Name of the certification authority or company
#     3. Duration: Duration or timeline of the certification
#
# The components should be well written, to the point and should be appropriate for a resume.
# The skills, experience and projects (personal and/or company projects) should be aligned to the Job descriptions.
#
# """

class CompleteDataExtraction:
    def __init__(self, api_key):

        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=api_key,
            response_format=Resume
        )

    async def complete_resume_data_extractor(self, task):
        agent = AssistantAgent(
            name="ResumeDataExtractor",
            description="An Agent for extracting data from raw text",
            model_client=self.model_client
        )
        return await agent.run(task = task)

    # def executor_(self):
    #     with ThreadPoolExecutor() as executor:
    #         future1 = executor.submit(self.extract_candidate_info)
    #         return future1.result()


async def main():
    t = time()
    # api_key_gemini = os.getenv('GOOGLE_API_KEY')
    # model_name = "gemini-2.5-flash",
    # base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
    data_extraction = CompleteDataExtraction(
                                    # model_name=model_name,
                                    # base_url=base_url,
                                     api_key=api_key)

    response = await data_extraction.complete_resume_data_extractor(task)
    # response = await data_extraction.extract_certification_info()
    print(response)
    # print(data_extraction.candidate_info_summary)
    print("Time taken - ", time() - t)
    x = 1

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    model_name = "gemini-2.5-flash",
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
    asyncio.run(main())
    # response = data_extraction.executor_()
    # print(response)

