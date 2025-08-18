from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console

import asyncio
import sys
sys.path.append("..")

# from DataExtraction.CompleteResumeExtraction import CompleteDataExtraction
from DataExtraction.ComponentWiseResumeExtraction import ComponentWiseDataExtraction
from model.ResumeModel import Resume

from dotenv import load_dotenv
import os

load_dotenv()

class ResumeHandler:

    def __init__(self):

        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4o",
            api_key=os.getenv('OPEN_API_KEY')
        )
        self.model_resume_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv('OPEN_API_KEY'),
            response_format=Resume
        )

        # self.complete_data_extraction = CompleteDataExtraction(os.getenv('OPEN_API_KEY'))
        self.componentWiseDataExtraction = ComponentWiseDataExtraction()

        # self.planning_model_client = OpenAIChatCompletionClient(
        #     model="gpt-4o",
        #     api_key=os.getenv('OPEN_API_KEY')
        # )

        self.combined_termination = TextMentionTermination('TERMINATE') | MaxMessageTermination(max_messages=20)

        self.planning_agent = AssistantAgent(
            name="PlanningAgent",
            description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
            model_client=self.model_client,
            system_message="""
            You are a planning agent.
            Your job is to break down complex tasks into smaller, manageable subtasks.
            Your team members are:
                CompleteResumeExtractionAgent: Extracts the resume data from raw text data
                ComponentWiseResumeExtractionAgent: Extracts the resume data from raw text data for different sections
    
            You only plan and delegate tasks - you do not execute them yourself.
    
            When assigning tasks, use this format:
            1. <agent> : <task>
    
            After all tasks are complete, summarize the findings and end with "TERMINATE".
            """,
        )

        self.complete_extraction_agent = AssistantAgent(
            name="ResumeCompleteDataExtractor",
            description="An Agent for extracting complete information from raw text",
            model_client=self.model_resume_client
        )

        self.component_wise_extraction_agent = AssistantAgent(
            name="ResumeComponentWiseDataExtractor",
            description="An Agent for extracting component wise information from primary resume data extraction",
            model_client=self.model_resume_client
        )

        self.component_group_chat_prompt = """
        Select an agent to perform the task.
        
        {roles}
        
        current conversation history :
        {history}
        
        Read the above conversation, then select an agent from {participants} to perform the next task.
        Make sure that the planning agent has assigned task before other agents start working.
        Only select one agent.
        """

        self.component_wise_data_extraction_group_chat = SelectorGroupChat(
            participants=[self.componentWiseDataExtraction.candidateDataExtractorAgent,
                          self.componentWiseDataExtraction.educationDataExtractorAgent,
                          self.componentWiseDataExtraction.companyProjectDataExtractorAgent,
                          self.componentWiseDataExtraction.personalProjectDataExtractorAgent,
                          self.componentWiseDataExtraction.experienceDataExtractorAgent,
                          self.componentWiseDataExtraction.certificationDataExtractorAgent
                          ],
            model_client=self.model_client,
            termination_condition=self.combined_termination,
            selector_prompt=self.component_group_chat_prompt,
            allow_repeated_speaker=True)

        self.component_wise_data_extraction_society_of_mind_agent = SocietyOfMindAgent("component_wise_data_extraction_society_of_mind",
                                                        team=self.component_wise_data_extraction_group_chat,
                                                        model_client=self.model_client,
                                                        response_prompt='Update the missing resume components which could not be extracted earlier.')

    async def process_resume(self, task):
        selector_prompt = '''
        Select an agent to perform the task.
        
        {roles}
        
        current conversation history :
        {history}
        
        Read the above conversation, then select an agent from {participants} to perform the next task.
        Make sure that the planning agent has assigned task before other agents start working.
        Only select one agent.
        '''

        self.selector_team = SelectorGroupChat(
            participants=[self.planning_agent, self.complete_extraction_agent, self.component_wise_data_extraction_society_of_mind_agent],
            model_client=self.model_client,
            termination_condition=self.combined_termination,
            selector_prompt=selector_prompt,
            allow_repeated_speaker=True)

        # response = self.selector_team.run_stream(task=task)
        response = await Console(self.selector_team.run_stream(task=task))
        print(response)


if __name__ == "__main__":
    resumeHandler = ResumeHandler()
    # response = resumeHandler.process_resume()
    task = """
    Please extract information from the below raw resume data.
    1. Extract the complete information.
    2. if some of components are not extracted well then extract the missing information component wise.

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
    # task = "Who was the Miami Heat player with the highest point in the 2006-2007 season, and what was the percentage change in his total rebounds between the 2007-2008 and 2008-2009 seasons?"
    asyncio.run(resumeHandler.process_resume(task))
