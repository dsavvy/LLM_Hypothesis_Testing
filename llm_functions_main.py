# In this document, we define the functions that the PythonApp will call to do actions with the LLM.


# 1. Step 

# Call the LLM with the message list
response = llm.invoke([
    {"content": "Translate the prompt to Italian", "role": "system"},
    {"content": "What is the capital of France?", "role": "user"}
])
parser.invoke(response)
print(response)
