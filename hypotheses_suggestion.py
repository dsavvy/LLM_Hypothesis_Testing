# Import LLM query utility
from llm_instruction import llm_query

# Import Streamlit and custom modules for building UI and responses
import streamlit as st
import Streamlit_build as app

# Import image handling and I/O tools
from PIL import Image as PILImage
from io import BytesIO
import requests
import json
import pandas as pd

# Import function to generate a textual description of directly-follows relations
from diagram_generateDFG import GenTextualAbstraction

# Import custom module for querying SIGNAL
import signal_queries as signalq


# Fetch an image from Signavio, save it locally, and display it in the Streamlit app
def showProcess(cookies, headers):
    # Read credential data needed for the Signavio endpoint
    with open('signavio-credentials.txt') as f:
        sk = json.load(f)
    system_instance = sk["system_instance"]
    revision_id = "1fe7397c17304d3ba4ea41f1eefc97fe"
    diagram_url = system_instance + '/p/revision'
    # Request a PNG of a process diagram from the provided URL
    png_request = requests.get(
        f'{diagram_url}/{revision_id}/png',
        cookies=cookies,
        headers=headers
    )
    print(png_request)
    # Convert the request content into an image object
    image = PILImage.open(BytesIO(png_request.content))
    png_path = './graph.png'
    # Write the retrieved PNG content to a local file
    with open(png_path, 'wb') as f:
        f.write(png_request.content)
    # Convert images with alpha channels to RGB with a white background
    if image.mode in ("RGBA", "LA"):
        white_background = PILImage.new("RGBA", image.size, "WHITE")
        image = PILImage.alpha_composite(white_background, image).convert("RGB")
    # Display the diagram in the Streamlit interface
    st.image(image, caption="Process Diagram of the most common process flow within the example event log.")
    return image


# Present the user with choices to define a direction for subsequent analysis
def selectDirection():
    # If there's no direction saved in session state, initialize it
    if "direction" not in st.session_state:
        st.session_state["direction"] = ""
    app.response("Please select in which direction you want to build a hypothesis.")
    # Button: Data Quality
    if st.button("Check Data Quality", key="data_check"):
        st.session_state["direction"] = "Check Data Quality"
        st.session_state.messages.append({
            "role": "user",
            "content": "I want to check Data Quality"
        })
    # Button: Process Conformance
    if st.button("Check Process Conformance", key="conf_check"):
        st.session_state["direction"] = "Check Process Conformance"
        st.session_state.messages.append({
            "role": "user",
            "content": "I want to Check Process Conformance"
        })
    # Button: Enhance Process Model
    if st.button("Enhance Process Model", key="enhance_model"):
        st.session_state["direction"] = "Enhance Process Model"
        st.session_state.messages.append({
            "role": "user",
            "content": "I want to look for optimization opportunities"
        })
    # Provide feedback if no direction has been chosen yet
    if not st.session_state["direction"]:
        app.response("Please select hypothesis 1, 2, or 3 by the respective button.")
    return st.session_state["direction"]


# Suggest multiple hypotheses for the chosen direction by querying the LLM with relevant context
def suggestHypothesis(direction):
    # Feed the user's chosen direction into a query function
    app.query(f"{'I want to '} {direction}")
    # Generate textual abstraction of the DFG for context
    DFG_relation = GenTextualAbstraction()
    # Build a query for an event log sample
    signal_eventlog_query = (
        "SELECT case_id, event_name, end_time, Activity, Resource, elementId, "
        "\"lifecycle:transition\", \"org:resource\", resourceCost, resourceId "
        "FROM \"defaultview-4\" LIMIT 1"
    )
    event_log_exc = signalq.query_signal(signal_eventlog_query)
    # Construct system messages for the LLM
    sysgenDFG = (
        "We are conducting statistical hypothesis testing as part of Process Mining. "
        "'Your task is to generate three hypotheses, and then SQL querys. Next, you "
        "will find the textual abstraction of the directly follows relations in the process: "
    )
    sys_message_gen = f"{sysgenDFG}{DFG_relation}{'. '}"
    sysgenlog = " Furthermore, you must consider the data format. This is an example query that includes all columns of the event log: "
    sys_message_gen = f"{sys_message_gen}{sysgenlog}{signal_eventlog_query}{'. '}"
    sysgenlog2 = "This is the result of this query showing all columns of the event log: "
    sysgenx = "The following text will provide you with some context about hypothesis testing in Process Mining, and for what it is used: "
    # Read a local file that explains hypothesis testing in process mining
    with open("./hypothesis_suggestion_context.txt", "r") as file:
        context = file.read()
    sys_message_gen = f"{sys_message_gen}{sysgenx}{context}{'. '}"
    sysgen3 = (
        "Now, create three hypothesis in natural language based on the data provided. "
        "In Process Mining, we use hypothesis to test either test the quality of the "
        "data in the event log, check if the event log data conforms to our process model, "
        "or to find enhancements to the process. You will build hypothesis to test the following direction: "
    )
    sys_message_gen = f"{sys_message_gen}{sysgenlog2}{event_log_exc}{sysgen3}{direction}{'. '}"
    sysgen4 = "Try to make the hypotheses as simple and specific as possible so we can convert them into simple, directly executable SQL queries later."
    sys_message_gen = f"{sys_message_gen}{direction}{sysgen4}{'. '}"
    sys_message_user = "I am building three hypotheses ideas in natural language we can use to investigate the described process."
    # Send the constructed messages to the LLM and capture the answer
    answer = llm_query(sys_message_gen, sys_message_user)
    answer = answer['answer']
    app.response(answer)
    # Store both direction and answer in a file for later reference
    with open("./hypothesis_options.txt", "a") as file:
        file.write(direction)
        file.write(answer)
    return answer


# Allow the user to pick one of the three generated hypotheses and persist the choice
def choose_hypothesis(options):
    # Each button queries the LLM to extract just the relevant hypothesis text
    if st.button("Select Hypothesis 1", key="hyp_1"):
        st.session_state.selected_hypothesis = llm_query(
            "Extract Hypothesis 1. Only extract and return the first hypothesis, and nothing else.", 
            options
        )
    elif st.button("Select Hypothesis 2", key="hyp_2"):
        st.session_state.selected_hypothesis = llm_query(
            "Extract Hypothesis 2. Only extract and return the second hypothesis, and nothing else.", 
            options
        )
    elif st.button("Select Hypothesis 3", key="hyp_3"):
        st.session_state.selected_hypothesis = llm_query(
            "Extract Hypothesis 3. Only extract and return the third hypothesis, and nothing else.", 
            options
        )
    # If a hypothesis was chosen, write it to file and return it
    if "selected_hypothesis" in st.session_state and st.session_state.selected_hypothesis:
        with open("./hypothesis_gen.txt", "a") as file:
            st.session_state.selected_hypothesis = ", ".join(
                f"{key}: {value}" for key, value in st.session_state.selected_hypothesis.items()
            )
            file.write(st.session_state.selected_hypothesis)
        return st.session_state.selected_hypothesis
    return "Error: No hypothesis selected."


# Load definitions of certain metrics from JSON, build a small DataFrame, and store it in another JSON
def ExtractExampleQueries():
    files = ["cycle_time.json"]
    rows = []
    for file in files:
        with open(f"./metric_definitions/{file}", "r") as file:
            metric = json.load(file)
        for metric in metric['metrics']:
            description = metric['description']
            signal_fragment = metric['signalFragment']
            rows.append({"Description": description, "SIGNAL_code": signal_fragment})
    query_df = pd.DataFrame(rows)
    json_table = query_df.to_dict(orient="index")
    with open("./example_queries.json", "w") as file:
        json.dump(json_table, file)


# Execute the data-extraction function as soon as the script runs
ExtractExampleQueries()
