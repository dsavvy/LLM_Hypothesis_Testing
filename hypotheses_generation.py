# Imports core functions to interact with the LLM, Streamlit, and signal queries
from llm_instruction import llm_query
from llm_instruction import llm_query
import Streamlit_build as app
import signal_queries as signalq
import json

def generate_query(hypothesis):
    # Builds a system prompt describing the hypothesis and available columns
    sysgen1 = "You are conducting statistical hypothesis testing as part of Process Mining. You have the following hypothesis: "
    sys_message_gen = f"{sysgen1}{hypothesis}"
    sysgen2 = "Your task provided by the user message will be to transform this hypothesis into a valid SQL query. You will execute it on our database with the following column names: "
    signal_eventlog_query = 'SELECT CASE_ID, EVENT_NAME, END_TIME, Activity, Resource, elementId, ' \
                            '"lifecycle:transition", "org:resource", resourceCost, resourceId ' \
                            'FROM FLATTEN("defaultview-4") LIMIT 20'
    sys_message_gen = f"{sys_message_gen}{sysgen2}{signal_eventlog_query}"

    # Obtains sample data from the database and appends it to the system prompt
    sysgen3 = "This data base request provided you with the correct column names. This is the result of the query from which you can determine the data types and formats in each column: "
    event_log_exc = signalq.query_signal(signal_eventlog_query)
    sys_message_gen = f"{sys_message_gen}{sysgen3}{event_log_exc}"

    # Writes this system prompt to a local file for reference
    with open("./system_messages/hypothesis_generation.txt", "a") as file:
        file.write(sys_message_gen)

    # Sends the prompt to the model, capturing only the SQL query from the result
    sys_message_user = "Transform this hypothesis into a valid SQL query with valid syntax..."
    app.query("I want to generate a SQL query from the hypothesis.")
    query = llm_query(sys_message_gen, sys_message_user)
    query = query['answer']
    query = query.strip()

    # Shows and stores the final SQL query
    app.response("This is the generated SQL query: " + query)
    with open("./hypothesis_query.txt", "a") as file:
       file.write(query)
    
    return query

def generate_query_SIGNAL_new(hypothesis):
    # Builds a system prompt describing the hypothesis and referencing SIGNAL syntax
    sysgen1 = "You are conducting statistical hypothesis testing as part of Process Mining. You have the following hypothesis: "
    sys_message_gen = f"{sysgen1}{hypothesis}"
    sysgen2 = "You are going to generate an SIGNAL query to work on my event log database..."
    signal_eventlog_query = "SELECT case_id, event_name, end_time, Activity, Resource, elementId, \"lifecycle:transition\", \"org:resource\", resourceCost, resourceId FROM \"defaultview-4\" LIMIT 1"
    sys_message_gen = f"{sys_message_gen}{sysgen2}{signal_eventlog_query}"

    # Fetches sample data to illustrate column contents and appends to the prompt
    sysgen3 = "The query returns the following result. This will show you the data contained in each column: "
    event_log_exc = signalq.query_signal(signal_eventlog_query)
    sys_message_gen = f"{sys_message_gen}{sysgen3}{event_log_exc}"

    # Reads a local SIGNAL documentation file and appends it to the prompt
    sysgen4 = "Next, you receive an extensive documentation of the SIGNAL processing language..."
    with open("./SIGNAL_documentation.txt", "r") as file:
        documentation = file.read()
    sys_message_gen = f"{sys_message_gen}{sysgen4}{documentation}"

    # Writes the entire prompt to a local file and queries the model
    with open("./system_messages/hypothesis_generation.txt", "a") as file:
        file.write(sys_message_gen)
    usergen = "Transform this hypothesis into a valid SIGNAL query to execute on our database..."
    sys_message_user = usergen
    app.query("I want to generate a SIGNAL query from the hypothesis.")
    query = llm_query(sys_message_gen, sys_message_user)
    query = query['answer']
    query = query.strip()

    # Sends final query to the UI and stores in a text file
    app.response("This is the generated SIGNAL query: " + query)
    with open("./hypothesis_query.txt", "a") as file:
       file.write(query)
    
    return query

def generate_query_SIGNAL(hypothesis):
    # Creates a system prompt showing the hypothesis and exemplary SIGNAL query
    sysgen1 = "You are conducting statistical hypothesis testing as part of Process Mining. You have the following hypothesis: "
    sys_message_gen = f"{sysgen1}{hypothesis}"
    sysgen2 = "You are going to generate an SIGNAL query to work on my event log database..."
    signal_eventlog_query = "SELECT case_id, event_name, end_time, Activity, Resource, elementId, \"lifecycle:transition\", \"org:resource\", resourceCost, resourceId FROM \"defaultview-4\" LIMIT 1"
    sys_message_gen = f"{sys_message_gen}{sysgen2}{signal_eventlog_query}"

    # Adds example output to clarify columns and data
    sysgen3 = "The query returns the following result. This will show you the data contained in each column: "
    event_log_exc = signalq.query_signal(signal_eventlog_query)
    sys_message_gen = f"{sys_message_gen}{sysgen3}{event_log_exc}"

    # Incorporates special SIGNAL features and constraints
    sysgen4 = 'SIGNAL is based on SQL, but is specifically designed for Process Intelligence...'
    sys_message_gen = f"{sys_message_gen}{sysgen4}"
    sysgen5 = 'Do not use JOIN. Do not use the WITH operator. '
    sysgen6 = ('There are additional functions in SIGNAL you can use: MATCHES... ')
    sysgen7 = ('The “~>” stands for "eventually follows". "->" stands for "directly follows". ')
    sys_message_gen = f"{sys_message_gen}{sysgen6}{sysgen7}"

    # Appends sample SIGNAL queries from a local JSON file
    sysgen8 = "To help you generate, here are some example queries that are valid in the SIGNAL process language: "
    with open("./example_queries.json", "r") as file:
        queries = json.load(file)
    sys_message_gen = f"{sys_message_gen}{sysgen8}{queries}"

    # Writes prompt to a local file, queries the model, and cleans up the result
    with open("./system_messages/hypothesis_generation.txt", "a") as file:
        file.write(sys_message_gen)
    usergen = "Transform this hypothesis into a valid SIGNAL query to execute on our database..."
    sys_message_user = usergen
    app.query("I want to generate a SIGNAL query from the hypothesis.")
    query = llm_query(sys_message_gen, sys_message_user)
    query = query['answer']
    query = query.strip()

    # Displays the query and saves it to a local text file
    app.response("This is the generated SIGNAL query: " + query)
    with open("./hypothesis_query.txt", "a") as file:
       file.write(query)
    
    return query
