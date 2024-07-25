import sys
import os
sys.path.append("../")
import SignavioAuthenticator
import requests
from IPython.display import Image, display
import json
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)



system_instance = 'https://academic.signavio.com'
tenant_id = '08f05dbc86024c3ca561dafd9d6d1186'
workspace_id = "08f05dbc86024c3ca561dafd9d6d1186"
user_name = "dominik.sawallisch@s.wu.ac.at"
pw = "sHHABrt5r_b"
revision_id = '807a789a020a4a2493b9fcde041a6bde'

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

