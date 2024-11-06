# In this document, we define the functions that the PythonApp will call to do actions with the LLM.
import sys
import os
sys.path.append("../")
import SignavioAuthenticator
import requests
from IPython.display import Image, display
import json
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
from PIL import Image as PILImage
from io import BytesIO
sys.path.append(os.path.abspath("/home/domi/Documents/VSC_Github/LLM_Hypothesis_Testing/bpmn2constraints"))
from bpmnconstraints.script import compile_bpmn_diagram
# 1 Provide Hypothesis Ideas
# Desc: Based on event log data, and the hypothesis ideas .csv from Signavio the LLM can provide an initial list of hypothesis.
# Context 1: Details about the investigated process (What process, what steps are included? - work from diagram)
# Context 2: The relevant Hypothesis Ideas from the CSV -> Adjust, categorize, load into Python.
# Context 3: A fitting System Message.

# Initialization: Send these and a tbd user message to the LLM, show the response in the GUI on a button press.


# 1: PROVIDE HYPOTHESIS IDEAS
def generate_ideas(cookies, headers, llm):
    # 0 authenticate 
    cookies = cookies
    headers = headers
    with open('signavio-credentials.txt') as f:
        sk = json.load(f)
    #Define variables needed for API access from the .txt's JSON.
    system_instance = sk["system_instance"]
    # 1 Request Process Details in JSON format
    # This is the revision ID that determines which process we access. We acquire it through website inspection via web developer tools.
    revision_id = "1fe7397c17304d3ba4ea41f1eefc97fe"
    # Request the BPMN diagram metadata for that revision_id.
    diagram_url = system_instance + '/p/revision'
    json_request = requests.get(
        f'{diagram_url}/{revision_id}/json',
        cookies=cookies,
        headers=headers)
    json_diagram = json_request.content

    # save the diagram metadata to diagram.json
    path = './diagram.json'
    with open(path, 'w') as f:
        json.dump(json.loads(json_diagram), f)
    
    # 1.1 Generate and request DFG graph from API
    ideas ="Hello World"
    
    
    return ideas

def generate_constraints():
    path = './diagram.json'
    declare_constraints = compile_bpmn_diagram(path, "DECLARE", False)
    return declare_constraints

def generate_png():
    path = './graph.png'
    

def signal_query(cookies, headers):
    cookies = cookies
    headers = headers
    with open('signavio-credentials.txt') as f:
        sk = json.load(f)
    system_instance = sk["system_instance"]        
    signal_endpoint = system_instance + '/g/api/pi-graphql/signal'
    request = requests.post(
        signal_endpoint,
        cookies=cookies,
        headers=headers,
        json={'query': 'SELECT COUNT(CASE_ID) FROM "defaultview-4"'})
    raw_result = request.json()
    with open("./result.json", "w") as file:
        json.dump(raw_result, file, indent=4)    
    result = request.json()['data'][0][0]
    print(result)
    return result





