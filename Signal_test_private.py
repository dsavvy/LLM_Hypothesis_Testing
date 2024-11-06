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



# 1. AUTHENTICATE WITH SIGNAVIO API

# Load API credentials from external text file.
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


# 2. GET DIAGRAM JSON
# This is the revision ID that determines which process we access. We acquire it through website inspection via web developer tools.
revision_id = "1fe7397c17304d3ba4ea41f1eefc97fe"
# Request the BPMN diagram metadata for that revision_id.




print(diagram_url)
json_request = requests.get(
    f'{diagram_url}/{revision_id}/json',
    cookies=cookies,
    headers=headers)
print(json_request)
json_diagram = json_request.content

# save the diagram metadata to diagram.json
path = './diagram.json'
with open(path, 'w') as f:
    json.dump(json.loads(json_diagram), f)


#3. GET DIAGRAM PNG for the process associated with the revision_id.
png_request = requests.get(
    f'{diagram_url}/{revision_id}/png',
    cookies=cookies,
    headers=headers)
print(png_request)
image = PILImage.open(BytesIO(png_request.content))
image.show()
# Save the .png file to the current directory.
png_path = './graph.png'
with open(png_path, 'wb') as f:
    f.write(png_request.content)

# 4. COMPILE VARIOUS CONSTRAINTS FROM THE DIAGRAM FOR TESTING
declare_constraints = compile_bpmn_diagram(path, "DECLARE", False) 
ltlf_constraints = compile_bpmn_diagram(path, "LTLF", False)   
signal_constraints = compile_bpmn_diagram(path, "SIGNAL", False)


# Defines a SIGNAL query template for checking constraint violations.
def signal_template(constraint):
    return f'SELECT COUNT(CASE_ID) FROM "defaultview-4" WHERE NOT event_name MATCHES{constraint}'

# Check for Constraint Violations vie Signal API
# Endpoint for POST request
signal_endpoint = system_instance + '/g/api/pi-graphql/signal'
constraint_violations = {}
for constraint in signal_constraints:
    query_request about:blank#blocked= requests.post(
        signal_endpoint,
        cookies=cookies,
        headers=headers,
        json={'query': signal_template(constraint)})
    if 'data' in query_request.json(): constraint_violations[constraint] = query_request.json()['data'][0][0]
# print(constraint_violations)


# 5. GET NUMBER OF CASES AND CONFORMANCE RATE
count_request = requests.post(
    signal_endpoint,
    cookies=cookies,
    headers=headers,
    json={'query': 'SELECT COUNT(CASE_ID) FROM "defaultview-4"'})
case_count = count_request.json()['data'][0][0]
print(case_count)

# 6. PRINT RESULTS
print("Number of violations", constraint_violations["(^'review request')"])
print("Conformance rate", (1 - constraint_violations["(^'review request')"] / case_count) * 100, " %")


