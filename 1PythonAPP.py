# Import the main Streamlit library for building the web interface
import streamlit as st
# Import a custom module that initializes Streamlit and displays responses
import Streamlit_build as app
# Import a module that handles loading and storing of Signavio credentials
import signal_credentials as signal
# Import utility functions for showing process data and generating hypotheses
from hypotheses_suggestion import showProcess, suggestHypothesis, choose_hypothesis, selectDirection
# Import functions that generate different types of queries based on hypotheses
from hypotheses_generation import generate_query, generate_query_SIGNAL, generate_query_SIGNAL_new

# Define the main function that coordinates the entire application flow
def main():
    # Initialize Streamlit settings and configurations
    app.initialize_streamlit()
    # Send a welcome message to the interface
    app.response("Welcome! I am your LLM agent. I will help you generate hypotheses and code to investigate your process.")

    # Check and set default values for session state variables if they don't exist
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "investigation_started" not in st.session_state:
        st.session_state.investigation_started = False
    if "signal_cookies" not in st.session_state:
        st.session_state.signal_cookies = None
    if "signal_headers" not in st.session_state:
        st.session_state.signal_headers = None
    # Initialize an empty string for direction
    direction=""

    # Display a subheader for collecting Signavio credentials
    st.subheader("Signavio Credentials")
    # Load any existing credentials from the custom signal_credentials module
    credentials = signal.load_credentials()
    # Text input field for user name, pre-filled if available
    user_name = st.text_input("User Name", value=credentials.get("user_name", ""))
    # Text input field for password, masked by default
    password = st.text_input("Password", value=credentials.get("pw", ""), type="password")
    # Retrieve tenant ID from the loaded credentials
    tenant_id = credentials.get("tenant_id", "")

    # Create a button to trigger the authentication process
    if st.button("Authenticate"):
        try:
            # Attempt to authenticate with given tenant, username, and password
            auth_data = signal.st_signal_authenticate(tenant_id, user_name, password)
            # Store returned cookies in session state
            st.session_state.signal_cookies = auth_data['cookies']
            # Store returned headers in session state
            st.session_state.signal_headers = auth_data['headers']
            # Mark authentication as successful
            st.session_state.authenticated = True
            # Notify the user of successful authentication
            st.success("Successfully authenticated!")
        except Exception as e:
            # If an error occurs, display it and mark authentication as failed
            st.error(f"Authentication failed: {e}")
            st.session_state.authenticated = False

    # Only show process selection if user is authenticated
    if st.session_state.authenticated:
        # Display a subheader for selecting the process to investigate
        st.subheader("Process Selection")
        # Provide a text input for the process (revision) ID
        revision_id = st.text_input("Process ID", "1fe7397c17304d3ba4ea41f1eefc97fe", key="revision_id")

        # Button to start the process investigation
        if st.button("Start Investigation"):
            # Indicate the process data is being fetched
            st.success("Fetching process data...")
            try:
                # Show or load process data using the stored cookies and headers
                showProcess(st.session_state.signal_cookies, st.session_state.signal_headers)
                # Mark the investigation as started
                st.session_state.investigation_started = True
            except Exception as e:
                # Show an error if fetching fails, mark investigation as not started
                st.error(f"Could not fetch process data: {e}")
                st.session_state.investigation_started = False

    # Proceed if process data has been successfully fetched
    if st.session_state.investigation_started:
        # Check if direction has already been stored; if not, determine and store it
        if "direction" not in st.session_state:
            st.session_state.direction = selectDirection()
            app.response(st.session_state.direction)

        # Check if hypothesis options exist in session state; if not, suggest them
        if "hyp_options" not in st.session_state:
            st.session_state.hyp_options = suggestHypothesis(st.session_state.direction)
            app.response(st.session_state.hyp_options)

        # Check if a hypothesis has been selected; if not, provide selection interface
        if "selected_hypothesis" not in st.session_state:
            chosen_hyp = choose_hypothesis(st.session_state.hyp_options)
            if chosen_hyp != "Error: No hypothesis selected.":
                st.session_state.selected_hypothesis = chosen_hyp
            app.response(f"You selected the hypothesis: {st.session_state.selected_hypothesis}")

        # Generate and store a SQL query if not already in session state
        if "SQL_query" not in st.session_state:
            query = generate_query(st.session_state.selected_hypothesis)
            st.session_state.SQLquery = query
            with open("./session_output.txt", "a") as file:
                file.write(f"{st.session_state.selected_hypothesis}\n{query}\n")

        # Generate and store a SIGNAL query if not already in session state
        if "SIGNAL_query" not in st.session_state:
            SIGNAL_query = generate_query_SIGNAL(st.session_state.selected_hypothesis)
            st.session_state.SIGNALquery = SIGNAL_query
            with open("./session_output.txt", "a") as file:
                file.write(f"{st.session_state.selected_hypothesis}\n{SIGNAL_query}\n")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()