import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_agentchat.agents import AssistantAgent
from concurrent.futures import ThreadPoolExecutor
from time import time

from system_prompts import candidate_system_message

task = """
Please extract information from the below raw resume data.

** Resume Content **
PDF Miner

Prashant Singh
Roll No.: xxxxxxx
Bachelor of Technology
Shri Ramdeobaba College of Engineering and Management, Nagpur

(cid:131) +91-xxxxxxxx
# prashantxxxxx@gmail.com
§ GitHub Profile
(cid:239) LinkedIn Profile

Education

•Bachelor of Technology in Computer Science and Engineering(Cyber Security)
Shri Ramdeobaba College of Engineering and Management, Nagpur

2020-24

CGPA: xx

Personal Projects

•Web Based Facial Authentication(Liveness Detection)
A website based facial authentication system, implemented using a Chrome Extension.

– Facilitating users’ logins to websites without having to remember their credentials
– Used Live detection techniques to create high order security.
– Technology Used: Python, Reactjs, Bootstrap.

•Realtime Chat App
A react based web application which allow users to chat in real time.

– Used Firebase Authentication(SDK) to facilitate authentication & Cloud Firestore to store data.
– Technology Used: Reactjs, Firebase, Bootstrap, HTML.

•Covid-19 Tracker
Daily and weekly updated statistics tracking the number of COVID-19 cases, recovered, and deaths.

– Tracking world-wide cases using google maps and live API stats and datasets.
– Technology Used : JavaScript , CSS, HTML, API.

Experience

•AWS Cloud Virtual Internship
Online
AICTE-Eduskills
– In-depth understanding of AWS cloud computing services, including EC2, S3, RDS, Lambda, IAM, VPC, and

May - July 2023

more.

– Proficient in designing, deploying, and managing fault-tolerant, highly available, and scalable AWS solutions.
– Strong knowledge of architectural best practices, such as AWS Well-Architected Framework, security, performance,

and cost optimization.

– Hands-on experience in cloud infrastructure provisioning, monitoring, and automation using AWS Management

Console and AWS CLI.

•Palo Alto Cybersecurity Virtual Internship
AICTE-Eduskills
– Learned the fundamentals of Security Operations Center (SOC).
– Learned basics of Network & Cloud Security.

Technical Skills and Interests

Dec 2022 - Feb 2023

Online

Languages: C/C++, Python, Javascript, HTML+CSS
Libraries : C++ STL, Python Libraries, ReactJs
Web Dev Tools: Nodejs, VScode, Git, Github
Frameworks: ReactJs
Cloud/Databases:MongoDb, Firebase, Relational Database(mySql)
Relevent Coursework: Data Structures & Algorithms, Operating Systems, Object Oriented Programming, Database
Management System, Software Engineering.
Areas of Interest: Web Design and Development, Cloud Security.
Soft Skills: Problem Solving, Self-learning, Presentation, Adaptability

Positions of Responsibility

•On Desk Registrations Volunteer Aarhant Cyber Week Event - RCOEM, Nagpur

Oct - Dec 2022

– Helped to attract close to 300 attendees to the event.
– Collected over Rs. 20,000 in entry fees for different activities.

"""

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
            model = "gemini-2.5-flash",
            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key = api_key
        )

    complete_resume_system_message = """
    You are a resume analyzer.
    
    An ideal resume can contain the below components:
    
    ** A. Candidate information **
        1. Name: Name of the person
        2. Contact number: Contact number of the person
        3. Email address: Email address of the person
        4. LinkedIn ID: link to the LinkedIn profile of the person
        5. GitHub ID: link to the Github profile of the person
    ** B. Education information **
        1. Institution name: Name of the institution/college/school
        2. Marks: Marks/CGPA received from the institution/college/school
        3. Location: Location of the institution/college/school
        4. Duration: Duration or timeline of the education
    ** C. Company Project information **
        1. Project name: Name of the project
        2. Project description: Short description of the project
        3. Complete description: Complete descriptions of the project
        4. Technology: Duration or timeline of the education
        5. Duration: Duration or timeline of the project
    ** D. Personal Project information **
        1. Project name: Name of the project
        2. Project description: Short description of the project
        3. Complete description: Complete descriptions of the project
        4. Technology: Duration or timeline of the education
        5. Duration: Duration or timeline of the project
    ** E. Experience information **
        1. Company name: Name of the company the person worked with
        2. Designation: Designation name for the person in the company
        3. Contributions: Contributions or works done in the project
        4. Technology: Technologies, tools or softwares used in the company
        5. Duration: Duration or timeline for the experience in the company
    ** F. Certification information **
        1. Certification name: Name of the certification
        2. Certification Authority: Name of the certification authority or company
        3. Duration: Duration or timeline of the certification
    
    The components should be well written, to the point and should be appropriate for a resume.
    The skills, experience and projects (personal and/or company projects) should be aligned to the Job descriptions. 
    
    """

    # async def complete_resume_rating(self):
    #     agent = AssistantAgent(
    #         name="ResumeRater",
    #         description="An Agent for analysing resume and providing an overall rating along with component wise rating",
    #         model_client=self.model_client,
    #         system_message=candidate_system_message
    #     )
    #     return await agent.run(task=task)

    async def extract_candidate_info(self):
        agent = AssistantAgent(
            name="CandidateDataExtractor",
            description="An Agent for extracting the candidate information from the resume",
            model_client=self.model_client,
            system_message=candidate_system_message
        )
        self.candidate_info_summary = await agent.run(task=task)


    # async def extract_education_info(self):
    #     agent = AssistantAgent(
    #         name="EducationDataExtractor",
    #         description="An Agent for extracting the education information from the resume",
    #         model_client=self.model_client,
    #         system_message=education_system_message
    #     )
    #     self.education_info_summary = await agent.run()
    #
    # async def extract_company_projects_info(self):
    #     agent = AssistantAgent(
    #         name="CompanyProjectDataExtractor",
    #         description="An Agent for extracting the company project information from the resume",
    #         model_client=self.model_client,
    #         system_message=project_system_message
    #     )
    #     self.company_project_info_summary = await agent.run()
    #
    # async def extract_personal_projects_info(self):
    #     agent = AssistantAgent(
    #         name="PersonalProjectDataExtractor",
    #         description="An Agent for extracting the personal project information from the resume",
    #         model_client=self.model_client,
    #         system_message=personal_project_system_message
    #     )
    #     self.personal_project_info_summary = await agent.run()
    #
    # async def extract_experience_info(self):
    #     agent = AssistantAgent(
    #         name="ExperienceDataExtractor",
    #         description="An Agent for extracting the experience information from the resume",
    #         model_client=self.model_client,
    #         system_message=experience_system_message
    #     )
    #     self.experience_info_summary = await agent.run()
    #
    # async def extract_certification_info(self):
    #     agent = AssistantAgent(
    #         name="CertificationDataExtractor",
    #         description="An Agent for extracting the experience information from the resume",
    #         model_client=self.model_client,
    #         system_message=certification_system_message
    #     )
    #     self.certifications_info_summary = await agent.run()

    def executor_(self):
        with ThreadPoolExecutor() as executor:
            future1 = executor.submit(self.extract_candidate_info)
            return future1.result()


async def main():
    t = time()
    api_key_gemini = os.getenv('GOOGLE_API_KEY')
    model_name = "gemini-2.5-flash",
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
    data_extraction = DataExtraction(model_name=model_name, base_url=base_url, api_key=api_key_gemini)

    await data_extraction.complete_resume_rating()
    print(data_extraction.candidate_info_summary)
    print("Time taken - ", time() - t)

if __name__ == "__main__":
    load_dotenv()
    api_key_gemini = os.getenv('GOOGLE_API_KEY')
    model_name = "gemini-2.5-flash",
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
    asyncio.run(main())
    # response = data_extraction.executor_()
    # print(response)

