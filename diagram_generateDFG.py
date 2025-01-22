from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
import streamlit as st
import Streamlit_build as app
from PIL import Image as PILImage
from io import BytesIO
import requests
import json




# MAKE JSON SHORTER; CONVERT IT TO STRING TO MAKE SURE WE GET A RESULT HERE! THE JSON FORMAT MIGHT BE AN ISSUE ACTUALLY MORE THAN THE LENGTH :D


#This function extracts the events, and directly follows relations from the event log
def generateJSON():
    # Remove first three lines once its implemented in the Python App.
    signal_auth_data = signal.signal_authenticate()
    cookies = signal_auth_data['cookies']
    headers = signal_auth_data['headers']
    #Define variables for SIGNAL
    with open('signavio-credentials.txt') as f:
        sk = json.load(f)
    system_instance = sk["system_instance"]
    revision_id = "1fe7397c17304d3ba4ea41f1eefc97fe"
    diagram_url = system_instance + '/p/revision'
    # Make the JSON request
    json_request = requests.get(
        f'{diagram_url}/{revision_id}/json',
        cookies=cookies,
        headers=headers)
    json_diagram = json_request.content
    path = './diagram.json'
    with open(path, 'w') as f:
        json.dump(json.loads(json_diagram), f)
    # Now we have an up-to-date diagram at diagram.json and as variable json_diagram


   # 1. Remove everything up to child shapes from level 1
    # Level 2: Childshapes numbered 0-24. Keep everything.
    # Level 3: Keep: Outgoing - that references connections via their IDs. Keep: resourceID. Target: references connection as well.
    # Level 3: Keep: stencil. Keep: Properties, 
    # Level 3: Remove: formats, dockers, labels, bounds, layers, glossaryLinks, labelDirtyStates, childShapes, labels
    # Properties: Only keep outmsgitemkind, looptype, instantiate, inmsgitemkind, onebehavioreventref, behavior, nonebehavioreventref, name_de_de, name, implementation	 
def generateDFG():
    with open("./diagram.json", "r") as f:
        data = json.load(f)  # Pass the file object 'f' instead of 'json'
    
    # Define properties to keep at level 3
    level_3_properties_to_keep = ["nonebehavioreventref", "name", "name_de_de"]

    # Process level 2 childShapes
    def process_child_shapes(child_shapes):
        processed_shapes = []
        for shape in child_shapes[:25]:  # Keep shapes 0-24
            # Level 3 processing for each child shape in level 2
            level_3_shape = {
                "outgoing": shape.get("outgoing", []),
                "resourceId": shape.get("resourceId"),
                "stencil": shape.get("stencil", {}),
                "properties": {key: shape.get("properties", {}).get(key) for key in level_3_properties_to_keep}
            }
            processed_shapes.append(level_3_shape)
        return processed_shapes

    # Create the output structure
    output_data = {
        "childShapes": process_child_shapes(data.get("childShapes", []))
    }

    # Save output to a new JSON file
    with open("diagram_textualabstraction.json", "w") as file:
        json.dump(output_data, file, indent=4)
        
def textualabstraction():
    with open("diagram_textualabstraction.json", "r") as f:
        data = f.read()
    
    sys_message =("We are conducting Process Mining. You will receive a textual abstraction of the events, and their relations to each other in JSON format. From this, extract the events, and their associations with each other. From your textual output I should be able to draw a business process diagram without any further adjustments or thinking from my side. Choose an appropriate textual representation, only use standard characters, and only return that. Be as concise as possible. ")
    user_message = (data)
    response = llm_query(sys_message, user_message)
    response = response['answer']
    return response

def GenTextualAbstraction():
    generateJSON()
    generateDFG()
    response = textualabstraction()
    return response
        
             
        
 
    
    
    
        
    