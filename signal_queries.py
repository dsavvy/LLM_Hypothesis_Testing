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


def signal_authenticate():
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

    return cookies, headers, system_instance


def query_signal(query):
    cookies, headers, system_instance = signal_authenticate()
    signal_endpoint = system_instance + '/g/api/pi-graphql/signal'
    try:
        signal_request = requests.post(
            signal_endpoint,
            cookies=cookies,
            headers=headers,
            json={'query': query})
        signal_request.raise_for_status()  # Raise an error for bad status codes
        result = signal_request.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        result = "Request Exception"
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        result = "JSON Decode Error"
    #result = signal_request.json()['data'][0][0]
    return str(result)


    
test = query_signal('SELECT CASE_ID, EVENT_NAME, END_TIME, Activity, Resource, elementId, '
    '"lifecycle:transition", "org:resource", resourceCost, resourceId '
    'FROM "defaultview-4" LIMIT 1')
print(test)

