from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
from hypotheses_suggestion import suggestHypothesis

def evaluate_query():
    with open("./hypothesis_exec.txt", "r") as file:
        response = file.read() 
    with open("./hypothesis_query.txt", "r") as file:
        SQL_query = file.read()         
    sysgen = "You are conducting statistical hypothesis testing within Process Mining. We have executed the following query on our event log: "
    sysgen2 = "We got the following result: "
    sysgen_u = "Please interpret the result of the query in natural language, considering the original query."
    sys_message_gen = f"{sysgen}{SQL_query}{sysgen2}{response}"
    sys_message_user = sysgen_u
    query= llm_query(sys_message_gen, sys_message_user)
    interpretation = query['answer']
    interpretation = interpretation.strip()
    print(interpretation)
    with open("./hypothesis_interpret.txt", "w") as file:
       file.write(interpretation)
    return interpretation       