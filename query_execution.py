from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
from hypotheses_suggestion import suggestHypothesis
from hypotheses_generation import generate_query
import requests
import json


def execute_query(cookies, headers):
    with open('signavio-credentials.txt') as f:
        sk = json.load(f)
    system_instance = sk["system_instance"]
    signal_endpoint = system_instance + '/g/api/pi-graphql/signal'
    with open("./hypothesis_query.txt", "r") as file:
        query = file.read()   
    request = requests.post(
        signal_endpoint,
        cookies=cookies,
        headers=headers,
        json={'query': query})
    response = request.json()['data'][0][0]
    response_str = str(response) 
    with open("./hypothesis_exec.txt", "w") as file:
       file.write(response_str)
    return response