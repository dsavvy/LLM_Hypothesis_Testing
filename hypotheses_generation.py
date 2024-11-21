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
import signal_queries as signal


def generate_query():
    # This is the generated hypothesis in a text file
    with open("./hypothesis_gen.txt", "r") as file:
        hypothesis = file.read()

    sysgen1 = "You are conducting statistical hypothesis testing as part of Process Mining. You have the following hypothesis: "
    sys_message_gen = f"{sysgen1}{hypothesis}"
    sysgen2 = "You are going to generate an SQL query to work on my database. I will provide you with an exemplary SQL statement that explicitly all rows available so you know how to build the query: "
    signal_eventlog_query="SELECT CASE_ID, EVENT_NAME, END_TIME, Activity, Resource, elementId, \"lifecycle:transition\", \"org:resource\", resourceCost, resourceId FROM \"defaultview-4\" LIMIT 1"
    sys_message_gen = f"{sys_message_gen}{sysgen2}{signal_eventlog_query}"
    sysgen3 = "The query returns the following result. This will show you the data that is contained in each column, and its format: "
    event_log_exc = signal.query_signal(signal_eventlog_query)
    sys_message_gen = f"{sys_message_gen}{sysgen3}{event_log_exc}"
    with open("./system_messages/hypothesis_generation", "w") as file:
        file.write(sys_message_gen)
        
    usergen = "Transform this hypothesis into a valid SQL query to execute on our database given its column names, content, and structure. Make sure your query follows valid SQL syntax. Just return the generated query, and nothing else. Your result must be directly executable."    
    sys_message_user = usergen
    #print(sys_message_gen)

    query = llm_query(sys_message_gen, sys_message_user)
    query = query['answer']
    query = query.strip()
    app.response("This is the generated query: " + query)
    with open("./hypothesis_query.txt", "w") as file:
       file.write(query)
    
    return query   
    
