import streamlit as st
import Streamlit_build as app
import signal_credentials as signal
from hypotheses_suggestion import showProcess, suggestHypothesis, choose_hypothesis, selectDirection
from hypotheses_generation import generate_query, generate_query_SIGNAL

def main():
    # 0. Basic initialization
    app.initialize_streamlit()
    app.response("Welcome! I am your LLM agent. I will help you generate hypotheses and code to investigate your process.")

    # Make sure we have a place to store state flags/variables
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "investigation_started" not in st.session_state:
        st.session_state.investigation_started = False
    if "signal_cookies" not in st.session_state:
        st.session_state.signal_cookies = None
    if "signal_headers" not in st.session_state:
        st.session_state.signal_headers = None
    direction="" 

    # 1. Collect and authenticate credentials
    st.subheader("Signavio Credentials")
    credentials = signal.load_credentials()
    user_name = st.text_input("User Name", value=credentials.get("user_name", ""))
    password = st.text_input("Password", value=credentials.get("pw", ""), type="password")
    tenant_id = credentials.get("tenant_id", "")

    if st.button("Authenticate"):
        try:
            auth_data = signal.st_signal_authenticate(tenant_id, user_name, password)
            st.session_state.signal_cookies = auth_data['cookies']
            st.session_state.signal_headers = auth_data['headers']
            st.session_state.authenticated = True
            st.success("Successfully authenticated!")
        except Exception as e:
            st.error(f"Authentication failed: {e}")
            st.session_state.authenticated = False

    # 2. Proceed only if authenticated
    if st.session_state.authenticated:
        st.subheader("Process Selection")
        revision_id = st.text_input("Process ID", "1fe7397c17304d3ba4ea41f1eefc97fe", key="revision_id")
        
        if st.button("Start Investigation"):
            st.success("Fetching process data...")
            try:
                # Show or retrieve process info, store if needed
                showProcess(st.session_state.signal_cookies, st.session_state.signal_headers)
                st.session_state.investigation_started = True
            except Exception as e:
                st.error(f"Could not fetch process data: {e}")
                st.session_state.investigation_started = False

    # 3. If the process data is fetched, proceed with hypothesis steps
    if st.session_state.investigation_started:
        # (A) Choose direction only once
        if "direction" not in st.session_state:
            st.session_state.direction = selectDirection()
            app.response(st.session_state.direction)
            
        
        # (B) Show possible hypotheses only once
        if "hyp_options" not in st.session_state:
            st.session_state.hyp_options = suggestHypothesis(st.session_state.direction)
            app.response(st.session_state.hyp_options)
        # (C) Let user pick from the hypotheses via choose_hypothesis
        #     Only pick if we haven't already
        if "selected_hypothesis" not in st.session_state:
            chosen_hyp = choose_hypothesis(st.session_state.hyp_options)
            if chosen_hyp != "Error: No hypothesis selected.":
                st.session_state.selected_hypothesis = chosen_hyp
            app.response(f"You selected the hypothesis: {st.session_state.selected_hypothesis}")


        if "SQL_query" not in st.session_state:
            query = generate_query(st.session_state.selected_hypothesis)
            st.session_state.SQLquery = query
            with open("./session_output.txt", "a") as file:
                file.write(f"{st.session_state.selected_hypothesis}\n{query}\n")
        
        if "SIGNAL_query" not in st.session_state:
            SIGNAL_query = generate_query_SIGNAL(st.session_state.selected_hypothesis)
            # New function with _new is available
            st.session_state.SIGNALquery = SIGNAL_query
            with open("./session_output.txt", "a") as file:
                file.write(f"{st.session_state.selected_hypothesis}\n{SIGNAL_query}\n")


if __name__ == "__main__":
    main()
