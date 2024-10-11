from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
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

# 0.1 Initialize LLM: We set up the LLM
#llm = LLM.SAPLLM()

# 0.2 We initialize LangChain monitoring for the session.
#LANGCHAIN_TRACING_V2 = True
#LANGCHAIN_ENDPOINT="https://eu.api.smith.langchain.com"
#LANGCHAIN_API_KEY="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"
#LANGCHAIN_PROJECT="Thesis"

# Option to save messages from Langchain:
## llm_memory = MemorySaver()
## Transforms the response, if in a message format, into the simple response string.
## parser = StrOutputParser()





# X. With this function, we call the LLM API and print the response.

#NEXT: Make a Template: Each function will provide its own system function, completing the template. 
# The user will provide the content for the user message.
# 3. We pass the past messages also as part of the user message to the LLM.