from llm_instruction import llm_query
import signal_credentials
import os
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM



# 1. CREATION OF APP AGENT
# 1a We create a place where we can store the question answer pairs of a given session.
llm = LLM.SAPLLM()
llm_memory = MemorySaver()

# We set up LangSmith to inspect how our Application is working
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"




# With this function, we initiate a session with our Signal API. We do not define the revision_id yet. 
signal_credentials = signal_credentials.signal_authenticate()
signal_cookies = signal_credentials['cookies']
signal_headers = signal_credentials['headers']


# 1. With this function, we call the LLM API and print the response.
Response = llm.invoke("Tell me a funny insult to a German")
print(Response)
# COntinue here