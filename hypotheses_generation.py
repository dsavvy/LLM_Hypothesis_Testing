from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
from hypotheses_suggestion import suggestHypothesis
import Streamlit_build as app


def generate_query():
    with open("./hypothesis_gen.txt", "r") as file:
        hypothesis = file.read()

    sysgen1 = "You are conducting statistical hypothesis testing as part of Process Mining. You have the following hypothesis: "
    sysgen2 = "Transform this hypothesis into a valid SQL query. Make sure your query follows valid SQL syntax. Just return the generated query, and nothing else."
    sys_message_gen = f"{sysgen1}{hypothesis}"
    sys_message_user = sysgen2
    #print(sys_message_gen)

    query = llm_query(sys_message_gen, sys_message_user)
    query = query['answer']
    query = query.strip()
    app.response("This is the generated query: " + query)
    with open("./hypothesis_query.txt", "w") as file:
       file.write(query)
    
    return query   
    
