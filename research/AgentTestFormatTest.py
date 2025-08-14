import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_agentchat.agents import AssistantAgent

load_dotenv()
api_key_gemini = os.getenv('GOOGLE_API_KEY')

model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key_gemini,
)


from typing import Annotated, List
from pydantic import Field, BaseModel


class Operation(BaseModel):
    numbers: Annotated[List[int], Field(description="List of the numbers that will be used")]
    operation_type: Annotated[str, Field(description="Type of the operation")]


planning_agent = AssistantAgent(
    name="MathAgent",
    description="An Agent for performing math operations",
    model_client=model_client,
    system_message="""
    Your are Math agent.
    Your job is to detect the number to be used in the operation and the type of the operation

    After the tasks is complete, end with "TERMINATE".
    """,
    output_content_type=Operation
)

task = """
Detect the numbers and operation type from below,
** Add 2 with 3 **
"""

async def main():
    response = await planning_agent.run(task=task)
    x = 1

if (__name__ == '__main__'):
    asyncio.run(main())