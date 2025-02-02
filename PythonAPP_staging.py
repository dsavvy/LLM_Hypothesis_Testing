from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
import json
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
from hypotheses_suggestion import showProcess, suggestHypothesis, choose_hypothesis
from hypotheses_generation import generate_query
from query_execution import execute_query
from query_evaluation import evaluate_query
import streamlit as st
import Streamlit_build as app
# USE: streamlit run /home/domi/Documents/VSC_Github/LLM_Hypothesis_Testing/PythonAPP_staging.py



# 0. We set up the environment for the App.
# 0.1 We set up the GUI for the user.
# 1. We use functions from llm_functions_main to call functions to and from the LLM.
# 2. We use functions from signavio_functions_main to call functions to and from the Signavio API.
# 3. We use both to create the process/program flow depicted in the Process Manager.

# 0: SETTING UP THE ENVIRONMENT
# 0.1 Initialize Signavio:
#   We authenticate with Signavio and assign the cookies, and headers.

signal_auth_data = signal.signal_authenticate()
signal_cookies = signal_auth_data['cookies']
signal_headers = signal_auth_data['headers']

# We initialize Streamlit and show a welcome message. 
app.initialize_streamlit()
app.response("Welcome to our prototype! I am your LLM assistant and will help you to conduct statistical hypothesis tests to learn more about your process. Let us start mining!")
# 1. SELECT INITIAL HYPOTHESIS
# 1.0 We show the user the most common process flow.
graph = showProcess(signal_cookies, signal_headers)
# 1.1 Suggest three Hypotheses for the user to choose from


hyp_options = suggestHypothesis()
# 1.2 Let the user select one of the three hypotheses via three buttons.
hypothesis = choose_hypothesis(hyp_options)
# End result: Initial Hypothesis selected; Stored under variable "hypothesis" and in file "hypothesis_gen.txt"

# Only start this, once we have populated the hypothesis.
if isinstance(hypothesis, str):
    app.response("You selected the hypothesis: " + hypothesis)
    app.response("Now, the agent generates a query to test this hypothesis.")

# 2. We generate a valid SIGNAL Query to test the hypothesis.
# requirements for LLM: knowledge of the process, the hypothesis, and the constraints.
# 2.2 We need the structure of the event log - open!
# 2.3 We probably need to know the specifics of Signal within the system message.

query = generate_query()
# This outputs a response with the query in the app.

with open("./session_output.txt", "a") as file:
    file.write(f"{hypothesis}\n{query}\n")


# 3. We execute the query on the event log.
#PQL_response = execute_query(signal_cookies, signal_headers)
#print(PQL_response)


# 4. We evaluate the query result and transform it back to natural language.
#PQL_eval = evaluate_query()
#print(PQL_eval)

# Save all of the results to my text file.
#with open("./session_output.txt", "a") as file:
#    file.write(f"{hypothesis}\n{query}\n{PQL_response}\n{PQL_eval}\n")









# X. With this function, we call the LLM API and print the response.

#NEXT: Make a Template: Each function will provide its own system function, completing the template. 
# The user will provide the content for the user message.
# 3. We pass the past messages also as part of the user message to the LLM.