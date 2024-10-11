from langchain.llms.base import LLM
import requests
import llm_credentials
from typing import List, Optional
import llm_credentials as cred
from langchain_core.language_models.llms import LLM



class SAPLLM(LLM):
    # Here, we explain the the LLM we are using is Llama 3 deployed via the SAP API.
    @property
    def _llm_type(self) -> str:
        return "Llama3_LLM_via_SAP"    
    # Get all the identifying parameters for our LLM
    @property
    def _identifying_params(self) -> dict:
        auth_token, resource_group = cred.get_llm_auth().values()
        endpoint = cred.get_llm_endpoint().values()
        
        return {
            "model_name": "meta--llama3-70b-instruct",
            'auth_token': auth_token[:5],
            'resource_group': resource_group[5:],
            'endpoint': endpoint
            }
        

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Reuse the logic from your function to make the request to the LLM endpoint
        if stop is not None:
            raise NotImplementedError("Stop tokens are not supported by this LLM API.")
        llm_deployment_url = 'https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/d59971ba56763962'
        endpoint = f"{llm_deployment_url}/chat/completions"
        auth_token, resource_group = llm_credentials.get_llm_auth().values()
        
        input_data = {
            "model": "meta--llama3-70b-instruct",
            "messages": [prompt]
        }
        print(input_data)

        headers = {
            "Authorization": f"Bearer {auth_token}",
            'ai-resource-group': resource_group,
            "Content-Type": "application/json"
        }
        
        response = requests.post(endpoint, headers=headers, json=input_data)
        response_json = response.json()
        # Extract the answer from the response JSON
        if "choices" in response_json and len(response_json["choices"]) > 0:
            response = response_json["choices"][0]["message"]["content"]
        else:
           raise ValueError("No answer found in the response.")
        
        return response