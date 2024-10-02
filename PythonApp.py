import json
import requests
import os
import llm_credentials
import llm_instruction



# 1. Get LLM Credentials
auth_token = llm_credentials.get_llm_auth()
llm_instruction.llm_query("Say Hello World")
# COntinue here