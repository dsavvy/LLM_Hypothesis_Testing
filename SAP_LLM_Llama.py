# Access through REST API

from ipywidgets import widgets
import json
import requests


# Define Resource Group
resource_group = widgets.Text(
    value='6c2265ed-4778-4a78-8433-033dd254ab69', # resource group
    placeholder='Resource Group',
    description='Provided Resource Group assigned by SAP',
    disabled=False
)
resource_group

# Define LLM Model Options
llm_model_name = widgets.Dropdown(
    options=[
        "meta--llama3-70b-instruct",
        "gpt-35-turbo",
        "gpt-4",
        "gpt-4-32k",
        "tiiuae--falcon-40b-instruct"
    ],
    value="meta--llama3-70b-instruct",
    description="LLM Model Name",
    disabled=False,
)


# Define Deployment ID
#deployment_id = widgets.Text(
    #value='d262055d9b56e698', # resource group
    #placeholder='Deployment ID for embedding model',
    #description='',
    #disabled=False
#)
#deployment_id

llm_deployment_url = widgets.Text(
    value='https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/d59971ba56763962', # resource group
    placeholder='Deployment URL for LLM',
    description='',
    disabled=False
)

# Secret Key Text File
with open('irpa-r1156-joint-master-thesi-sk.txt') as f:
    sk = json.load(f)


#Define variables needed for API access
auth_url = f"{sk['url']}/oauth/token"
client_id = sk['clientid']
client_secret = sk['clientsecret']
api_base_url = f"{sk['serviceurls']['AI_API_URL']}/v2"



response = requests.post(
    auth_url,
    data={"grant_type": "client_credentials"},
    auth=(client_id, client_secret),
    timeout=8000,
)
auth_token = response.json()["access_token"]
print(auth_token[:5])


# Preparing the input with parameters specified for inference
test_input = {
    "model" : llm_model_name.value,
    "messages": [
        {"content": "Tell me a joke about Generative AI", "role": "user"}
    ]
}

endpoint = f"{llm_deployment_url.value}/chat/completions" # endpoint implemented in serving engine
print(endpoint)

headers = {
    "Authorization": f"Bearer {auth_token}",
    'ai-resource-group': resource_group.value,
    "Content-Type": "application/json"
}
response = requests.post(endpoint, headers=headers, json=test_input)

response_json = response.json()
print(response_json)

# Extract and print the answer from the JSON response
if "choices" in response_json and len(response_json["choices"]) > 0:
    answer = response_json["choices"][0]["message"]["content"]
    print(answer)
else:
    print("No answer found in the response.")


