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
# Adds directories to Python's module search path  so bpmnconstraints.script can be imported.
sys.path.append(os.path.abspath("/home/domi/Documents/VSC_Github/LLM_Hypothesis_Testing/bpmn2constraints"))
from bpmnconstraints.script import compile_bpmn_diagram

# In This file, we use the Authenticator to provide an access token for the SIGNAL API.


def signal_authenticate():
    #   Load API credentials from external text file.
    with open('signavio-credentials.txt') as f:
        sk = json.load(f)
    #Define variables needed for API access from the .txt's JSON.
    system_instance = sk["system_instance"]
    tenant_id = sk["tenant_id"]
    workspace_id = sk["workspace_id"]
    user_name = sk["user_name"]
    pw = sk["pw"]
    # Use SignavioAuthenticator.py to authenticate with the Signavio API.
    authenticator = SignavioAuthenticator.SignavioAuthenticator(system_instance, tenant_id, user_name, pw)
    auth_data = authenticator.authenticate()
    print("authenticated!")
    #Sets cookies and headers for future API requests. These include session info (JSESSIONID, LBROUTEID) and an authentication token (x-signavio-id).  
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    return {
        'cookies': cookies,
        'headers': headers
    }
