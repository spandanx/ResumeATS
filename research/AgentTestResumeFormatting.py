import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_agentchat.agents import AssistantAgent
import json
from time import time

load_dotenv()
api_key_gemini = os.getenv('GOOGLE_API_KEY')

model_client = OpenAIChatCompletionClient(
    # model="gemini-1.5-flash",
    model = "gemini-2.5-flash",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key_gemini,
)


from typing import Annotated, List, Optional
from pydantic import Field, BaseModel

# class Resume(BaseModel):
#     # candidate_information: Candidate
#     # education: List[Education]
#     projects: List[Project] = Field(description="list of the projects done in the companies if available. Do not consider personal projects. Extract projects only if they are company projects, return empty list if not found")
#     personal_projects: List[Project] = Field(description="list of the personal projects mentioned in the resume is available. Consider only personal projects and do not consider company projects, return empty list if not found")
#     skills: List[str] = Field(description="Skills of the person")
#     experience: List[Experience] = Field(description="list of the company experiences available in the resume, return empty list if not found")
#     achievements: List[str] = Field(description="Achievements made or reward received during working in companies, return empty list if not found")
#     certifications: List[Certification] = Field(description="List of the certifications, return empty list if not found")


# planning_agent = AssistantAgent(
#     name="ResumeDataExtractor",
#     description="An Agent for extracting information from raw resume information",
#     model_client=model_client,
#     system_message="""
#     You are data extraction agent.
#     Your job is to read the raw text and format them based on the format instruction.
#
#     After the tasks is complete, end with "TERMINATE".
#     """,
#     output_content_type=Resume
# )

candidateDataExtractor = AssistantAgent(
    name="CandidateDataExtractor",
    description="An Agent for extracting the candidate information from the resume",
    model_client=model_client,
    system_message=candidate_system_message
)

# candidateDataExtractor = AssistantAgent(
#     name="CandidateDataExtractor",
#     description="An Agent for extracting the candidate information from the resume",
#     model_client=model_client,
#     system_message="""
#     You are data extraction agent.
#     Your job is to read the raw text and extract candidate information based on the format instruction.
#     """,
#     output_content_type=Candidate
# )

educationDataExtractor = AssistantAgent(
    name="educationDataExtractor",
    description="An Agent for extracting the education information from the resume",
    model_client=model_client,
    system_message="""
    You are data extraction agent.
    Your job is to read the raw text and extract education information based on the format instruction.
    Return and empty list if the required information is not available
    """,
    output_content_type=Education
)

projectDataExtractor = AssistantAgent(
    name="projectDataExtractor",
    description="An Agent for extracting the project information from the resume",
    model_client=model_client,
    system_message="""
    You are data extraction agent.
    Your job is to read the raw text and extract company project information based on the format instruction.
    List of the projects done in the companies if available. Do not consider personal projects.
    Extract projects only if they are company projects, return empty list if not found.
    """,
    output_content_type=Project
)

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage

team = RoundRobinGroupChat(
    participants=[candidateDataExtractor
        # , educationDataExtractor, projectDataExtractor
                  ],
    max_turns=1
)

async def run_team(instruction):
    task = TextMessage(content=instruction, source='user')
    result = await team.run(task=task)
    print(result)

instruction = """
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

async def main():
    # response = await planning_agent.run(task=task)
    # response = await run_team(instruction)
    t = time()
    response = await candidateDataExtractor.run(task=instruction)
    model_message = response.messages[-1].content
    print(model_message)
    x = 1
    print("Time taken - ", time() - t)

if (__name__ == '__main__'):
    asyncio.run(main())