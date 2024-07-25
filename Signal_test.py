import sys
import os
sys.path.append("../")
import SignavioAuthenticator
import requests
from IPython.display import Image, display
import json
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)



system_instance = 'https://editor.signavio.com'
tenant_id = '992552b41a33492abf1c3ab47bbe8ed0'
tenantID = '992552b41a33492abf1c3ab47bbe8ed0'
workspace_id = "992552b41a33492abf1c3ab47bbe8ed0"
user_name = 'dominik.sawallisch@sap.com'
pw = 'sHHABrt5r_s'
revision_id = 'aaee4b04526c4d8f996c7dbab93c6f14'

authenticator = SignavioAuthenticator.SignavioAuthenticator(system_instance, tenant_id, user_name, pw)
auth_data = authenticator.authenticate()

print("authenticated!")
cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
diagram_url = system_instance + '/p/revision'

json_request = requests.get(
    f'{diagram_url}/{revision_id}/json',
    cookies=cookies,
    headers=headers)
json_diagram = json_request.content
path = './diagram.json'
with open(path, 'w') as f:
    json.dump(json.loads(json_diagram), f)
png_request = requests.get(
    f'{diagram_url}/{revision_id}/png',
    cookies=cookies,
    headers=headers)
display(Image(png_request.content))

