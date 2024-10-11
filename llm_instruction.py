import llm_credentials
import requests
import json

# We use this file to define functions to set up the LLM API in terms of context, and to query the API after having done that. 

def llm_setup():
    
    
    
    return "hello"


# In the LLM Query, we need to do: 1. Provide System Prompt for context. 2. Provide previous User prompts (must be stored somewhere)!. 3. Append new prompt
def llm_query(sys_mes, user_mes):
    llm_deployment_url = 'https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/d59971ba56763962'
    endpoint = f"{llm_deployment_url}/chat/completions" # endpoint implemented in serving engine
    auth_token, resource_group = llm_credentials.get_llm_auth().values()
    input = {
        "model" : "meta--llama3-70b-instruct",
        "messages": [
            {"content": sys_mes, "role": "system"},
            {"content": user_mes, "role": "user"}
            
        ]        
    }
    print(input)  
    # We prepare the HTTP request header using our auth and specify the JSON content type.
    headers = {
    "Authorization": f"Bearer {auth_token}",
    'ai-resource-group': resource_group,
    "Content-Type": "application/json"
    }
    #Send prepared POST request to the endpoint using the header and input.
    response = requests.post(endpoint, headers=headers, json=input)
    response_json = response.json()
    with open("gen_response.json", "w") as file:
        json.dump(response_json, file, indent=4)
    # Extract and print the answer from the JSON response
    if "choices" in response_json and len(response_json["choices"]) > 0:
        answer = response_json["choices"][0]["message"]["content"]
    else:
        print("No answer found in the response.")
    # We return the question posted, and the answer by the LLM.    
    return {
        'answer': answer
    }
    