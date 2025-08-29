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
    task = {
        "resume_content": """
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
    }
    asyncio.run(resumeHandler.extract_resume(task))
