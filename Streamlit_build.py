import streamlit as st

# In this file, we contain all the code to build the streamlit app.
# We then initialize all at once by calling it as a function from the PythonApp.

def initialize_streamlit():
    # Define title of the app
    st.title("PM Hypothesis Testing App")
    # Set up an empty session state / chat history.
    st.session_state.messages = []
    # React to user input
    

def query(query):
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
 
def response(response):
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})    
    



#if prompt := st.chat_input("What is up?"):
#    # Display user message in chat message container
#    st.chat_message("user").markdown(prompt)
 #   # Add user message to chat history
  #  st.session_state.messages.append({"role": "user", "content": prompt})
#
 #   response = f"Echo: {prompt}"
  #  # Display assistant response in chat message container
   # with st.chat_message("assistant"):
#        st.markdown(response)
 #   # Add assistant response to chat history
  #  st.session_state.messages.append({"role": "assistant", "content": response})

    



