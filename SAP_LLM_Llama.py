# Access through REST API


import json
import requests




# 1. DEFINE VARIABLES AND CREDENTIALS

# Secret Key Text File
with open('sap-llm-credentials.txt') as f:
    sk = json.load(f)

# Define variables needed for API access. These come from the secret key text file.
# The Resource Group is the Unique ID provided to me by SAP. I use it to authenticate myself along with the secret key text file.
resource_group = sk['resource_group']
# This is the URL to authenticate the user with the API. It provides the client ID and secret key to get an access token.
auth_url = f"{sk['url']}/oauth/token"
client_id = sk['clientid']
client_secret = sk['clientsecret']
# We use out credentials to get an access token for the API.
response = requests.post(
    auth_url,
    data={"grant_type": "client_credentials"},
    auth=(client_id, client_secret),
    timeout=8000,
)
auth_token = response.json()["access_token"]

# We use the Open source Llama3 model for our code and specify the address where we access it for inference.
llm_deployment_url = 'https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/d59971ba56763962'
endpoint = f"{llm_deployment_url}/chat/completions" # endpoint implemented in serving engine


# 2. SPECIFY TEXT INPUT TO LLM.

# Preparing the input with parameters specified for inference.
# This must change into a DEF function where we specify the input into the "content".
# Furthermore, we need to DEF a function that gives the LLM the system prompt that I use.
test_input = {
    "model" : "meta--llama3-70b-instruct",
    "messages": [
        {"content": "Tell me a joke about Generative AI", "role": "user"}
    ]
}
# 3. MAKE REQUEST

# We prepare the HTTP request header using our auth and specify the JSON content type.
headers = {
    "Authorization": f"Bearer {auth_token}",
    'ai-resource-group': resource_group,
    "Content-Type": "application/json"
}
print(headers)
#Send prepared POST request to the endpoint using the header and input.
response = requests.post(endpoint, headers=headers, json=test_input)

response_json = response.json()
# Extract and print the answer from the JSON response
if "choices" in response_json and len(response_json["choices"]) > 0:
    answer = response_json["choices"][0]["message"]["content"]
    print(answer)
else:
    print("No answer found in the response.")


