from llm_instruction import llm_query
import signal_credentials
import os
from langgraph.checkpoint.memory import MemorySaver



# 1. CREATION OF APP AGENT
# 1a We create a place where we can store the question answer pairs of a given session.
llm_memory = MemorySaver()
Qu_Re_Pair = llm_query("Simply Respond with Hello World")
print(Qu_Re_Pair['answer'])
# 


# With this function, we initiate a session with our Signal API. We do not define the revision_id yet. 
signal_credentials = signal_credentials.signal_authenticate()
signal_cookies = signal_credentials['cookies']
signal_headers = signal_credentials['headers']https://outlook.live.com/calendar/0/view/month


# 1. With this function, we call the LLM API and print the response.
Qu_Re_Pair = llm_query("Simply Respond with Hello World")
print(Qu_Re_Pair['answer'])
# COntinue here