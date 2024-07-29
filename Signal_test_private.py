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
from bpmnconstraints.script import compile_bpmn_diagram


with open('signavio-credentials.txt') as f:
    sk = json.load(f)


#Define variables needed for API access
system_instance = sk["system_instance"]
tenant_id = sk["tenant_id"]
workspace_id = sk["workspace_id"]
user_name = sk["user_name"]
pw = sk["pw"]
revision_id = "1fe7397c17304d3ba4ea41f1eefc97fe"


authenticator = SignavioAuthenticator.SignavioAuthenticator(system_instance, tenant_id, user_name, pw)
auth_data = authenticator.authenticate()

print("authenticated!")

cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
diagram_url = system_instance + '/p/revision'

print(diagram_url)


json_request = requests.get(
    f'{diagram_url}/{revision_id}/json',
    cookies=cookies,
    headers=headers)
print(json_request)
json_diagram = json_request.content

path = './diagram.json'

with open(path, 'w') as f:
    json.dump(json.loads(json_diagram), f)

png_request = requests.get(
    f'{diagram_url}/{revision_id}/png',
    cookies=cookies,
    headers=headers)
print(png_request)
image = PILImage.open(BytesIO(png_request.content))
#image.show()
    
png_path = './graph.png'
with open(png_path, 'wb') as f:
    f.write(png_request.content)


declare_constraints = compile_bpmn_diagram(path, "DECLARE", False) 
ltlf_constraints = compile_bpmn_diagram(path, "LTLF", False)   
signal_constraints = compile_bpmn_diagram(path, "SIGNAL", False)

def signal_template(constraint):
    return f'SELECT COUNT(CASE_ID) FROM "defaultview-4" WHERE NOT event_name MATCHES{constraint}'

signal_endpoint = system_instance + '/g/api/pi-graphql/signal'
constraint_violations = {}
for constraint in signal_constraints:
    query_request = requests.post(
        signal_endpoint,
        cookies=cookies,
        headers=headers,
        json={'query': signal_template(constraint)})
    if 'data' in query_request.json(): constraint_violations[constraint] = query_request.json()['data'][0][0]
print(constraint_violations)

count_request = requests.post(
    signal_endpoint,
    cookies=cookies,
    headers=headers,
    json={'query': 'SELECT COUNT(CASE_ID) FROM "defaultview-4"'})
case_count = count_request.json()['data'][0][0]
print(case_count)

print("Number of violations", constraint_violations["(^'review request')"])
print("Conformance rate", (1 - constraint_violations["(^'review request')"] / case_count) * 100, " %")


