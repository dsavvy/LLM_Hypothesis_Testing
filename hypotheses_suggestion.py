from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
import streamlit as st
import Streamlit_build as app
from PIL import Image as PILImage
from io import BytesIO
import requests
import json
import pandas as pd
from diagram_generateDFG import GenTextualAbstraction
import signal_queries as signal

def showProcess(cookies, headers):
    with open('signavio-credentials.txt') as f:
        sk = json.load(f)
    #Define variables needed for API access from the .txt's JSON.
    system_instance = sk["system_instance"]
    revision_id = "1fe7397c17304d3ba4ea41f1eefc97fe"
    diagram_url = system_instance + '/p/revision'
    png_request = requests.get(
    f'{diagram_url}/{revision_id}/png',
    cookies=cookies,
    headers=headers)
    print(png_request)
    image = PILImage.open(BytesIO(png_request.content))
    # Save the .png file to the current directory.
    png_path = './graph.png'
    with open(png_path, 'wb') as f:
        f.write(png_request.content)
    st.image(image, caption="Process Diagram of the most common process flow within your event log.")
    return image


def suggestHypothesis():
    # 1: SELECT INITIAL HYPOTHESIS
    ##ideas =  f.generate_ideas(signal_cookies, signal_headers, llm)
    ##print(ideas)
    # 1.1: Generate DECLARE CONSTRAINTS: CONFUSED LLM; DEPRECATED FOR NOW
    #declare_constraints = func.generate_constraints()
    #declare_constraints_str = "\n".join(declare_constraints)
    #declare_constraints_str = declare_constraints_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ").replace("\n", " ")
    #file_path = "./process_declare_constraints.txt"
    #with open(file_path, "w") as file:
    #    file.write(declare_constraints_str)

    ##result = f.signal_query(signal_cookies, signal_headers)
    ##print(result)


    # 1.2: Generate DFG graph - Textual Abstraction
    DFG_relation = GenTextualAbstraction()

    # 1.3 Retrieve 1 line from the event log
    signal_eventlog_query="SELECT case_id, event_name, end_time, Activity, Resource, elementId, \"lifecycle:transition\", \"org:resource\", resourceCost, resourceId FROM \"defaultview-4\" LIMIT 1"
    event_log_exc = signal.query_signal(signal_eventlog_query)

    # 1.4 Build first LLM system message
    sysgenDFG = "We are conducting statistical hypothesis testing as part of Process Mining. 'Your task is to generate three hypotheses, and then SQL querys. Next, you will find the textual abstraction of the directly follows relations in the process: "
    sys_message_gen = f"{sysgenDFG}{DFG_relation}"
    sysgenlog = " Furthermore, you must consider the data format. This is an example query that includes all columns of the event log: "
    sys_message_gen=f"{sys_message_gen}{sysgenlog}{signal_eventlog_query}"
    sysgenlog2 = "This is the result of this query showing all columns of the event log: "
    sysgen1 = "Now, create three hypothesis in natural language based on the data provided. Try to make the hypotheses as simple and specific as possible so we can convert them into simple, directly executable SQL queries later."
    sys_message_gen=f"{sys_message_gen}{sysgenlog2}{event_log_exc}{sysgen1}"
    print(sys_message_gen)
    sys_message_user = "I am building three hypotheses ideas in natural language we can use to investigate the described process."
    app.response(sys_message_user)
    # We print the query to the chat window for the user to see
    
    # 1.5 Query the LLM with the system message and the user message
    answer = llm_query(sys_message_gen, sys_message_user)
    answer = answer['answer']
    app.response(answer)
    with open("./hypothesis_options.txt", "w") as file:
       file.write(answer)
    return answer


def choose_hypothesis(options):
    if st.button("Select Hypothesis 1", key="hyp_1"):
        with st.chat_message("user"):
            st.markdown("You selected hypothesis 1")
        st.session_state.messages.append({"role": "user", "content": "You selected hypothesis 1"})    
        hypothesis = options.split("**Hypothesis 1:**")[1].split("**Hypothesis 2:**")[0]
    elif st.button("Select Hypothesis 2", key="hyp_2"):
        with st.chat_message("user"):
            st.markdown("You selected hypothesis 2")
        st.session_state.messages.append({"role": "user", "content": "You selected hypothesis 2"})
        hypothesis = options.split("**Hypothesis 2:**")[1].split("**Hypothesis 3:**")[0]
    elif st.button("Select Hypothesis 3", key="hyp_3"):
        with st.chat_message("user"):
            st.markdown("You selected hypothesis 3")
        st.session_state.messages.append({"role": "user", "content": "You selected hypothesis 3"})
        hypothesis = options.split("**Hypothesis 3:**")[1]
    else:
        print("Invalid input. Please select hypothesis 1, 2, or 3 by the respective button.")
        hypothesis = "Error: No hypothesis selected."
    file_path = "./hypothesis_gen.txt"
    with open(file_path, "w") as file:
        file.write(hypothesis)
    return hypothesis

def ExtractExampleQueries():
    files = ["cycle_time.json"]
    
    rows = []
    
    
    for file in files:
        with open (f"./metric_definitions/{file}","r") as file:
            metric = json.load(file)
        for metric in metric['metrics']:
            description = metric['description']
            signal_fragment = metric['signalFragment']
            rows.append({"Description": description, "SIGNAL_code": signal_fragment})
    query_df = pd.DataFrame(rows)
    json_table = query_df.to_dict(orient="index")
    with open("./example_queries.json", "w") as file:
        json.dump(json_table, file)
        

ExtractExampleQueries()
    