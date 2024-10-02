import json
import os
import requests

# This file provides all functions to return the correct credentials for the SAP LLM API.


def get_llm_auth():
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
    
    return {
        'auth_token': auth_token,
        'resource_group': resource_group
    }

def get_llm_endpoint():
    llm_model_name = "meta--llama3-70b-instruct"
    llm_deployment_url = 'https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/d59971ba56763962'
    endpoint = f"{llm_deployment_url}/chat/completions" # endpoint implemented in serving engine
    return {
        'endpoint': endpoint
    }
    


