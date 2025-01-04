from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
import json
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
from hypotheses_suggestion import showProcess, suggestHypothesis, choose_hypothesis, selectDirection
from hypotheses_generation import generate_query
from query_execution import execute_query
from query_evaluation import evaluate_query
import streamlit as st
import Streamlit_build as app
# USE: streamlit run /home/domi/Documents/VSC_Github/LLM_Hypothesis_Testing/1PythonAPP.py

# 0 Setup: Initialize Streamlit
app.initialize_streamlit()

app.response("Welcome! I am your LLM agent. I will help you generate hypotheses, and exemplary code to investigate your process in depth.")
app.response("First, provide your Signavio credentials.")


# 1. Authenticate with Signavio
credentials = signal.load_credentials()
tenant_id = st.text_input("Tenant ID", value=credentials.get("tenant_id", ""))
user_name = st.text_input("User Name", value=credentials.get("user_name", ""))
pw = st.text_input("Password", value=credentials.get("pw", ""), type="password")
if st.button("Authenticate"):
    new_credentials = {"tenant_id": tenant_id, "user_name": user_name, "pw": pw}
    try:
        signal_auth_data = signal.st_signal_authenticate(tenant_id, user_name, pw)
        signal_cookies = signal_auth_data['cookies']
        signal_headers = signal_auth_data['headers']
        if signal_cookies:
            st.success("Successfully authenticated!")
            st.session_state.signal_cookies = signal_cookies
            st.session_state.signal_headers = signal_headers
            st.session_state.authenticated = True
            
        else:
            st.error("Authentication failed. Please rerun the app and provide different credentials or use the suggested ones.")
    except Exception as e:
        st.error(f"Authentication failed: {e}")

# Workaround: These cannot be saved where I need to press the button, otherwise it causes issues with streamlit.
signal_auth_data = signal.st_signal_authenticate(tenant_id, user_name, pw)
signal_cookies = signal_auth_data['cookies']
signal_headers = signal_auth_data['headers']     
# 1.1 Provide a graph of our process
app.response("In our prototype, we investigate an example event log to create a credit quote. The most common process flow is depicted below.")
graph = showProcess(signal_cookies, signal_headers)


app.response("We can use hypotheses to test multiple aspects. Most common are: \n 1. Data Quality Check: Testing the data quality of the event log \n 2. Conformance Checking: Testing deviations between observed and expected standard process behavior. \n 3. Enhancement: Finding outliers and aspects to improve the standard process model")
direction = selectDirection()
app.response(direction)

hyp_options = suggestHypothesis()





# 2. Select what you want to do with the process. 








