from ipywidgets import widgets
import json
import os
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
import llm_commons.proxy.base
from llm_commons.proxy.openai import ChatCompletion
from llm_commons.proxy.identity import AICoreProxyClient
from llm_commons.langchain.proxy import ChatOpenAI
from llm_commons.langchain.proxy import init_embedding_model

# import proxy base module
import llm_commons.proxy.base

# specify proxy version
llm_commons.proxy.base.proxy_version = "aicore"

# Define Resource Group
resource_group = widgets.Text(
    value='6c2265ed-4778-4a78-8433-033dd254ab69', # resource group
    placeholder='Resource Group',
    description='Provide Resource Group assigned by SAP',
    disabled=False
)
resource_group

# Define LLM Model Options
llm_model_name = widgets.Dropdown(
    options=[
        "gpt-35-turbo",
        "gpt-35-turbo-16k",
        "gpt-4",
        "gpt-4-32k",
        "tiiuae--falcon-40b-instruct"
    ],
    value="gpt-4",
    description="LLM Model Name",
    disabled=False,
)
llm_model_name


# Define Deployment ID
deployment_id = widgets.Text(
    value='d262055d9b56e698', # resource group
    placeholder='Deployment ID for embedding model',
    description='',
    disabled=False
)
deployment_id


# Secret Key Text File
with open('irpa-r1156-joint-master-thesi-sk.txt') as f:
    sk = json.load(f)

# Configure proxy for AI Core Deployment
os.environ['AICORE_LLM_AUTH_URL'] = sk['url']+"/oauth/token"
os.environ['AICORE_LLM_CLIENT_ID'] = sk['clientid']
os.environ['AICORE_LLM_CLIENT_SECRET'] = sk['clientsecret']
os.environ['AICORE_LLM_API_BASE'] = sk["serviceurls"]["AI_API_URL"]+ "/v2"
os.environ['AICORE_LLM_RESOURCE_GROUP'] = resource_group.value
os.environ['LLM_COMMONS_PROXY'] = 'aicore'
llm_commons.proxy.resource_group = os.environ['AICORE_LLM_RESOURCE_GROUP']
llm_commons.proxy.api_base = os.environ['AICORE_LLM_API_BASE']
llm_commons.proxy.auth_url = os.environ['AICORE_LLM_AUTH_URL']
llm_commons.proxy.client_id = os.environ['AICORE_LLM_CLIENT_ID']
llm_commons.proxy.client_secret = os.environ['AICORE_LLM_CLIENT_SECRET']



# Instantiate AICoreProxyClient object
aic_proxy_client = AICoreProxyClient()

aic_proxy_client.add_foundation_model_scenario(
    scenario_id="ies-foundation-models",
    config_names="*-*",
    prediction_url_suffix='/v1/chat/completions'
)


llm = ChatOpenAI(
    proxy_client=aic_proxy_client,
    proxy_model_name=llm_model_name.value,
    temperature=0.5,
    max_tokens=400,
    model_kwargs={
        "frequency_penalty": -2, "presence_penalty": -1
    }
)

template = "Tell me a joke about {topic}"
prompt = PromptTemplate(template=template, input_variables=["topic"])
llm_chain = prompt | llm

completion = llm_chain.invoke({"topic": "Generative AI"})

print(completion.content)



