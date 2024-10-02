import json
import requests
import os
import llm_credentials
import llm_instruction



# 1. Get LLM Credentials
Qu_Re_Pair = llm_instruction.llm_query("Simply Respond with Hello World")
print(Qu_Re_Pair['answer'])
# COntinue here