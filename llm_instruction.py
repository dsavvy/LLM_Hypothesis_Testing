import llm_credentials
import requests
import json

# We use this file to define functions to set up the LLM API in terms of context, and to query the API after having done that. 

def llm_setup():
    
    
    
    return "hello"


# In the LLM Query, we need to do: 1. Provide System Prompt for context. 2. Provide previous User prompts (must be stored somewhere)!. 3. Append new prompt
def llm_query(sys_mes, user_mes):
    llm_deployment_url = 'https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/ddbc1c41c752b64f'
    endpoint = f"{llm_deployment_url}/chat/completions" # endpoint implemented in serving engine
    auth_token, resource_group = llm_credentials.get_llm_auth().values()
    input = {
        "model" : "meta--llama3.1-70b-instruct",
        "messages": [
            {"content": sys_mes, "role": "system"},
            {"content": user_mes, "role": "user"}
            
        ]        
    } 
    # We prepare the HTTP request header using our auth and specify the JSON content type.
    headers = {
    "Authorization": f"Bearer {auth_token}",
    'ai-resource-group': resource_group,
    "Content-Type": "application/json"
    }
    #Send prepared POST request to the endpoint using the header and input.
    response = requests.post(endpoint, headers=headers, json=input)
    print(response)
    response_json = response.json()
    with open("gen_response.json", "w") as file:
        json.dump(response_json, file, indent=4)
    # Extract and print the answer from the JSON response
    if "choices" in response_json and len(response_json["choices"]) > 0:
        answer = response_json["choices"][0]["message"]["content"]
    else:
        answer =("No answer found in the response.")
        print(answer)
    # We return the question posted, and the answer by the LLM.    
    return {
        'answer': answer
    }
    