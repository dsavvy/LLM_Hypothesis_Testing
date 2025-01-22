from llm_instruction import llm_query
from llm_instruction import llm_query
import Streamlit_build as app
import signal_queries as signalq
import json


def generate_query(hypothesis):

    # 1. Provide context for what to do
    sysgen1 = "You are conducting statistical hypothesis testing as part of Process Mining. You have the following hypothesis: "
    sys_message_gen = f"{sysgen1}{hypothesis}"
    sysgen2 = "Your task provided by the user message will be to transform this hypothesis into a valid SQL query. You will execute it on our database with the following column names: "
    signal_eventlog_query = 'SELECT CASE_ID, EVENT_NAME, END_TIME, Activity, Resource, elementId, '
    '"lifecycle:transition", "org:resource", resourceCost, resourceId '
    'FROM "defaultview-4" LIMIT 1'
    sys_message_gen=f"{sys_message_gen}{sysgen2}{signal_eventlog_query}"
    sysgen3 = "This data base request provided you with the correct column names. This is the result of the query from which you can determine the data types and formats in each column: "
    event_log_exc = signalq.query_signal(signal_eventlog_query)
    sys_message_gen=f"{sys_message_gen}{sysgen3}{event_log_exc}"
    # Save the query to a text file
    with open("./system_messages/hypothesis_generation.txt", "a") as file:
        file.write(sys_message_gen)
        
    sys_message_user = "Transform this hypothesis into a valid SQL query with valid syntax to execute on our database given its column names, content, and structure. Make sure your query follows valid SQL syntax. Just return the generated query, and nothing else. Return simply and only your generated SQL query. Your result must be directly executable."    
    app.query("I want to generate a SQL query from the hypothesis.")
    query = llm_query(sys_message_gen, sys_message_user)
    query = query['answer']
    query = query.strip()
    app.response("This is the generated SQL query: " + query)
    with open("./hypothesis_query.txt", "a") as file:
       file.write(query)
    
    return query   




def generate_query_SIGNAL(hypothesis):
    # 1. Provide context for what to do
    sysgen1 = "You are conducting statistical hypothesis testing as part of Process Mining. You have the following hypothesis: "
    sys_message_gen = f"{sysgen1}{hypothesis}"
    # 2. Provide the exemplary select query that contains all available rows in the event log.
    sysgen2 = "You are going to generate an SIGNAL query to work on my event log database. I will provide you with an exemplary SIGNAL statement that explicitly states all rows available so you know how to build the query: "
    signal_eventlog_query="SELECT case_id, event_name, end_time, Activity, Resource, elementId, \"lifecycle:transition\", \"org:resource\", resourceCost, resourceId FROM \"defaultview-4\" LIMIT 1"
    sys_message_gen = f"{sys_message_gen}{sysgen2}{signal_eventlog_query}"
    # 3. Provide an exemplary result of the event log.
    sysgen3 = "The query returns the following result. This will show you the data that is contained in each column, and its format: "
    event_log_exc = signalq.query_signal(signal_eventlog_query)
    sys_message_gen = f"{sys_message_gen}{sysgen3}{event_log_exc}"
    # 4. Describe the paticularities of the SIGNAL language
    sysgen4 = ('SIGNAL is based on SQL, but is specifically designed for Process Intelligence. Always select FROM default-view4 as you see in the examples. The event log and the event info in it (end_date, etc.) is nested. Always use FLATTEN("default-view4") to mitigate that.')
    sys_message_gen = f"{sys_message_gen}{sysgen4}"
    # 5. Describe what NOT to use in SIGNAL language
    sysgen5 = ('Do not use JOIN. Do not use the WITH operator. ')
    # 6. Additional Functions in SIGNAL
    # 6.1 MATCHES
    sysgen6 = ('There are additional functions in SIGNAL you can use: MATCHES: E.g. if we are interested in analyzing all cases where an invoice has been posted and cleared: SELECT count(case_id) FROM "defaultview-4" WHERE event_name MATCHES (‘Post Invoice’ ~> ‘Clear Invoice’)')
    # 6.2 ~> Eventually Follows
    sysgen7 = ('The “~>” stands for "eventually follows". If we would be interested in all cases where Clear Invoice was directly occurring after Post Invoice, the query would look like the following: SELECT count(case_id) FROM THIS_PROCESS WHERE event_name MATCHES (‘Post Invoice’ -> ‘Clear Invoice’) On the Contast, "->" stands for "directly follows".')
    sys_message_gen = f"{sys_message_gen}{sysgen6}{sysgen7}"
    # 6. Provide 8 positive query examples from the metrics_definitions library.
    sysgen8 = "To help you generate, here are some example queries that are valid in the SIGNAL process language: "
    
    with open("./example_queries.json", "r") as file:
        queries = json.load(file)
    sys_message_gen = f"{sys_message_gen}{sysgen8}{queries}"
    with open("./system_messages/hypothesis_generation.txt", "a") as file:
        file.write(sys_message_gen)
        
    usergen = "Transform this hypothesis into a valid SIGNAL query to execute on our database given its column names, content, and structure. Make sure your query follows valid SQL syntax. Just return the generated query, and nothing else. Your result must be directly executable."    
    sys_message_user = usergen
    app.query("I want to generate a SIGNAL query from the hypothesis.")
    #print(sys_message_gen)

    query = llm_query(sys_message_gen, sys_message_user)
    query = query['answer']
    query = query.strip()
    app.response("This is the generated SIGNAL query: " + query)
    with open("./hypothesis_query.txt", "a") as file:
       file.write(query)
    
    return query   

