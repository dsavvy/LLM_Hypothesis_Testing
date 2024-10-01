import json
import os
import llm_credentials

# We use this file to define functions to set up the LLM API in terms of context, and to query the API after having done that. 

def llm_setup():
    return "hello"


# In the LLM Query, we need to do: 1. Provide System Prompt for context. 2. Provide previous User prompts (must be stored somewhere)!. 3. Append new prompt
def llm_query(llm_message):
    auth_token = llm_credentials.get_llm_auth()
    input = {
        "model" : "meta--llama3-70b-instruct",
        "messages": [
            {"content": llm_message, "role": "user"}
        ]
    }
    # We prepare the HTTP request header using our auth and specify the JSON content type.
    headers = {
    "Authorization": f"Bearer {auth_token}",
    'ai-resource-group': resource_group,
    "Content-Type": "application/json"
    }
    #Send prepared POST request to the endpoint using the header and input.
    response = requests.post(endpoint, headers=headers, json=test_input)
    response_json = response.json()
    # Extract and print the answer from the JSON response
    if "choices" in response_json and len(response_json["choices"]) > 0:
        answer = response_json["choices"][0]["message"]["content"]
        print(answer)
    else:
        print("No answer found in the response.")
    # We return the question posted, and the answer by the LLM.    
    return {
        question: llm_message,
        answer: answer
    }
    