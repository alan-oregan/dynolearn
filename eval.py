# install on first run
# python -m venv .venv
# pip install -r requirements
# pip install py-readability-metrics


from dotenv import load_dotenv

from langchain_community.llms import HuggingFaceEndpoint
from langchain import PromptTemplate

from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

from readability import Readability
from readability.exceptions import ReadabilityException

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

prompts = """How to get ready for school
How to identify shapes
How to read body language
How to understand facial expressions
How to share with others
How to empathise with others
How to handle identify emotions
How to deal with emotions
How to spell their name
How to solve a maze
How to tidy up
How to ask for help
How to brush teeth
How to use the toilet
How to deal with loud noises
How to deal with bright lights
How to deal with strong smells
How to make friends
How to help others"""

def write_to_file(llm_input, llm_output, scores):
    with open("text.txt", "a") as t:
        t.writelines(string)
        t.writelines("\n")

def flesch_wrapper(rd: Readability):
    try:
        return rd.flesch().score
    except(ReadabilityException):
        return -1

def flesch_kincaid_wrapper(rd: Readability):
    try:
        return rd.flesch_kincaid().score
    except(ReadabilityException):
        return -1

def ari_wrapper(rd: Readability):
    try:
        return rd.ari().score
    except(ReadabilityException):
        return -1
    
def coleman_liau_wrapper(rd: Readability):
    try:
        return rd.coleman_liau().score
    except(ReadabilityException):
        return -1

def dale_chall_wrapper(rd: Readability):
    try:
        return rd.dale_chall().score
    except(ReadabilityException):
        return -1

def gunning_fog_wrapper(rd: Readability):
    try:
        return rd.gunning_fog().score
    except(ReadabilityException):
        return -1
    
def linsear_write_wrapper(rd: Readability):
    try:
        return rd.lisear_write(rd)
    except(ReadabilityException):
        return -1
    
def smog_wrapper(rd: Readability):
    try:
        return rd.smog().score
    except(ReadabilityException):
        return -1
    
def spache_wrapper(rd: Readability):
    try:
        return rd.spache().score
    except(ReadabilityException):
        return -1

    
def statistics_wrapper(rd: Readability):
    try:
        return rd.statistics()
    except(ReadabilityException):
        return -1

def eval(llm_input: str, llm_output: str):
    rd = Readability(llm_output)
    scores = {
        "flesch" :  rd.flesch_wrapper(rd),
        "flesch_kincaid" : flesch_kincaid_wrapper(rd),
        "ari" : ari_wrapper(rd),
        "coleman_liau" : coleman_liau_wrapper(rd),
        "dale_chall" : dale_chall_wrapper(rd),
        "gunning_fog" : gunning_fog_wrapper(rd),
        "linsear_write" : linsear_write_wrapper(rd),
        "smog" : smog_wrapper(rd),
        "spache" : spache_wrapper(rd),
        "statistics" : statistics_wrapper(rd)
    }

    write_to_file(llm_input, llm_output, scores)
    return scores

for prompt in prompts.split():
    llm_input ={
                "name": "William",
                "age": 7,
                "reading_level": 2,
                "teaching_task": prompt
            }

    llm_output = tasks_chain.invoke(llm_input)
.score
    eval(llm_input, " ".join(llm_output))
