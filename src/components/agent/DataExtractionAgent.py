from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

import sys
sys.path.append("..")

from DataExtraction.CompleteDataExtraction import CompleteDataExtraction
from DataExtraction.ComponentWiseResumeExtraction import ComponentWiseDataExtraction


from dotenv import load_dotenv
import os

load_dotenv()

class ResumeHandler:

    def __init__(self):

        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4o",
            api_key=os.getenv('OPEN_API_KEY')
        )
        self.complete_data_extraction = CompleteDataExtraction()
        self.component_wise_data_extraction = ComponentWiseDataExtraction()

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

    def process_resume(self):
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
            participants=[self.planning_agent, self.complete_data_extraction.complete_resume_data_extractor, self.component_wise_data_extraction.],
            model_client=self.model_client,
            termination_condition=self.combined_termination,
            selector_prompt=selector_prompt,
            allow_repeated_speaker=True)