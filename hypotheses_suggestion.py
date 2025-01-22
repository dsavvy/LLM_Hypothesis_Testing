from llm_instruction import llm_query
import streamlit as st
import Streamlit_build as app
from PIL import Image as PILImage
from io import BytesIO
import requests
import json
import pandas as pd
from diagram_generateDFG import GenTextualAbstraction
import signal_queries as signalq

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
    if image.mode in ("RGBA", "LA"):
        white_background = PILImage.new("RGBA", image.size, "WHITE")
        image = PILImage.alpha_composite(white_background, image).convert("RGB")
    st.image(image, caption="Process Diagram of the most common process flow within the example event log.")
    return image

def selectDirection():
    if "direction" not in st.session_state:
        st.session_state["direction"] = ""

    app.response("Please select in which direction you want to build a hypothesis.")

    if st.button("Check Data Quality", key="data_check"):
        st.session_state["direction"] = "Check Data Quality"
        st.session_state.messages.append({
            "role": "user",
            "content": "I want to check Data Quality"
        })

    if st.button("Check Process Conformance", key="conf_check"):
        st.session_state["direction"] = "Check Process Conformance"
        st.session_state.messages.append({
            "role": "user",
            "content": "I want to Check Process Conformance"
        })

    if st.button("Enhance Process Model", key="enhance_model"):
        st.session_state["direction"] = "Enhance Process Model"
        st.session_state.messages.append({
            "role": "user",
            "content": "I want to look for optimization opportunities"
        })
    
    # Show fallback message if still not chosen
    if not st.session_state["direction"]:
        app.response("Please select hypothesis 1, 2, or 3 by the respective button.")

    return st.session_state["direction"]




def suggestHypothesis(direction):
    app.query (f"{"I want to "} {st.session_state["direction"]}")

    # 1.2: Generate DFG graph - Textual Abstraction
    DFG_relation = GenTextualAbstraction()

    # 1.3 Retrieve 1 line from the event log
    signal_eventlog_query="SELECT case_id, event_name, end_time, Activity, Resource, elementId, \"lifecycle:transition\", \"org:resource\", resourceCost, resourceId FROM \"defaultview-4\" LIMIT 1"
    event_log_exc = signalq.query_signal(signal_eventlog_query)

    # 1.4 Build first LLM system message
    sysgenDFG = "We are conducting statistical hypothesis testing as part of Process Mining. 'Your task is to generate three hypotheses, and then SQL querys. Next, you will find the textual abstraction of the directly follows relations in the process: "
    sys_message_gen = f"{sysgenDFG}{DFG_relation}{". "}"
    sysgenlog = " Furthermore, you must consider the data format. This is an example query that includes all columns of the event log: "
    sys_message_gen=f"{sys_message_gen}{sysgenlog}{signal_eventlog_query}{". "}"
    sysgenlog2 = "This is the result of this query showing all columns of the event log: "
    sysgenx = "The following text will provide you with some context about hypothesis testing in Process Mining, and for what it is used: "
    with open("./hypothesis_suggestion_context.txt", "r") as file:
        context = file.read()
    sys_message_gen = f"{sys_message_gen}{sysgenx}{context}{". "}"    
    sysgen3 = "Now, create three hypothesis in natural language based on the data provided. In Process Mining, we use hypothesis to test either test the quality of the data in the event log, check if the event log data conforms to our process model, or to find enhancements to the process. You will build hypothesis to test the following direction: "
    sys_message_gen=f"{sys_message_gen}{sysgenlog2}{event_log_exc}{sysgen3}{". "}"
    
    sysgen4 = "Try to make the hypotheses as simple and specific as possible so we can convert them into simple, directly executable SQL queries later."
    sys_message_gen = f"{sys_message_gen}{direction}{sysgen4}{". "}"
    sys_message_user = "I am building three hypotheses ideas in natural language we can use to investigate the described process."
    

    # We print the query to the chat window for the user to see
    
    # 1.5 Query the LLM with the system message and the user message
    answer = llm_query(sys_message_gen, sys_message_user)
    answer = answer['answer']
    app.response(answer)
    with open("./hypothesis_options.txt", "a") as file:
        file.write(direction)
        file.write(answer)
    return answer


def choose_hypothesis(options):
    """
    Returns the hypothesis string if any selection button is pressed.
    Otherwise returns 'Error: No hypothesis selected.'
    """
    
    # Check for button clicks
    if st.button("Select Hypothesis 1", key="hyp_1"):
        st.session_state.selected_hypothesis = llm_query("Extract Hypothesis 1. Only extract and return the first hypothesis, and nothing else.", options)
    elif st.button("Select Hypothesis 2", key="hyp_2"):
        st.session_state.selected_hypothesis = llm_query("Extract Hypothesis 2. Only extract and return the second hypothesis, and nothing else.", options)
    elif st.button("Select Hypothesis 3", key="hyp_3"):
        # Fix the small typo: use .split(), not a comma
        st.session_state.selected_hypothesis = llm_query("Extract Hypothesis 3. Only extract and return the third hypothesis, and nothing else.", options)
    # If a hypothesis was chosen, persist it to file
    if "selected_hypothesis" in st.session_state and st.session_state.selected_hypothesis:    
        with open("./hypothesis_gen.txt", "a") as file:
            st.session_state.selected_hypothesis = ", ".join(f"{key}: {value}" for key, value in st.session_state.selected_hypothesis.items())
            file.write(st.session_state.selected_hypothesis)
        return st.session_state.selected_hypothesis
    
    return "Error: No hypothesis selected."


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
    