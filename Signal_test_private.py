import sys
import os
sys.path.append("../")
import SignavioAuthenticator
import requests
from IPython.display import Image, display
import json
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)





authenticator = SignavioAuthenticator.SignavioAuthenticator(system_instance, workspace_id, user_name, pw)
auth_data = authenticator.authenticate()
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

