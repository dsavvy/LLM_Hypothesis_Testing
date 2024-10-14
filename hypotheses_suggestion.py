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



def suggestHypothesis():
    # 1: SELECT INITIAL HYPOTHESIS
    ##ideas =  f.generate_ideas(signal_cookies, signal_headers, llm)
    ##print(ideas)
    # 1.1: Generate DECLARE CONSTRAINTS
    declare_constraints = func.generate_constraints()
    declare_constraints_str = "\n".join(declare_constraints)
    declare_constraints_str = declare_constraints_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ").replace("\n", " ")
    file_path = "./process_declare_constraints.txt"
    with open(file_path, "w") as file:
        file.write(declare_constraints_str)

    ##result = f.signal_query(signal_cookies, signal_headers)
    ##print(result)


    # 1.2: Generate DFG graph - To-Do / question!
    # To-Do! / Ask Timotheus!

    # 1.3 Retrieve 1 line from the event log
    # To-Do! / Ask Timotheus!

    # 1.4 Build first LLM system message
    sysgen1 = "We are conducting statistical hypothesis testing as part of Process Mining. Your task is to generate three SQL querys. Next, you will find the declare constraints"
    sys_message_user = "I am building three hypotheses ideas in natural language we can use to investigate the process."
    sys_message_gen = f"{sysgen1}{declare_constraints_str}"
    # We print the query to the chat window for the user to see
    app.query(sys_message_user)
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
