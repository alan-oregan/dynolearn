# install on first run
# python -m venv .venv
# pip install -r requirements

from flask import Flask
from flask_restful import Resource, Api

from dotenv import load_dotenv

from langchain_community.llms import HuggingFaceEndpoint
from langchain import PromptTemplate

from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

hub = HuggingFaceEndpoint(repo_id="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")

tasks_template = """<|im_start|>system
You are a helpful designer for a childrens digital game company<|im_end|>
<|im_start|>user
{name} is {age} years old and has a reading level age of {reading_level}. They need help with {teaching_task}.

Make a list of 10 suitable game scene tasks to learn {teaching_task}.

Just list out each item 1 by 1 as a JSON list. Only provide the list of tasks, do not include the question or any other information, just the list of tasks.<|im_end|>
<|im_start|>assistant
"""

tasks_prompt = PromptTemplate(
    template = tasks_template,
    input_variables=["name", "age", "reading_level", "teaching_task"]
)

class Tasks(BaseModel):
    tasks: List = Field(description="list of game scene tasks")

parser = JsonOutputParser(pydantic_object=Tasks)

tasks_prompt_json = PromptTemplate(
    template=tasks_template,
    input_variables=["name", "age", "reading_level", "teaching_task"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

tasks_chain = tasks_prompt_json | hub | parser

app = Flask(__name__)
api = Api(app)

class tasks(Resource):
    def get(self):
        result = tasks_chain.invoke(
            {
                "name": "Alan",
                "age": 8,
                "reading_level": 2,
                "teaching_task": "How to deal with strong smells"
            }
        )
        return result

api.add_resource(tasks, '/')

if __name__ == '__main__':
    app.run(debug=True)
