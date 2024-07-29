import requests
import json
from IPython.display import Image, display
import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)

class SignavioAuthenticator:
    def __init__(self, system_instance, tenant_id, email, pw):
        self.system_instance = system_instance
        self.tenant_id = tenant_id
        self.email = email
        self.pw = pw

    """
    Takes care of authentication against Signavio systems
    """

    def authenticate(self):
        """
        Authenticates user at Signavio system instance and initiates session.
        Returns:
            dictionary: Session information
        """
        login_url = self.system_instance + "/p/login"
        data = {
            "name": self.email,
            "password": self.pw,
            "tokenonly": "true",
            "tenant": self.tenant_id
        }
        # authenticate
        login_request = requests.post(login_url, data=data)

        # retrieve token and session ID
        auth_token = login_request.content.decode("utf-8")
        jsesssion_ID = login_request.cookies.get("JSESSIONID", "")

        # The cookie is named 'LBROUTEID' for base_url 'editor.signavio.com'
        # and 'editor.signavio.com', and 'AWSELB' for base_url
        # 'app-au.signavio.com' and 'app-us.signavio.com'
        lb_route_ID = login_request.cookies.get("LBROUTEID", "")

        # return credentials
        return {
            "jsesssion_ID": jsesssion_ID,
            "lb_route_ID": lb_route_ID,
            "auth_token": auth_token,
        }

# Configuration
system_instance = 'https://editor.signavio.com'
tenant_id = '992552b41a33492abf1c3ab47bbe8ed0'
user_name = 'dominik.sawallisch@sap.com'
pw = 'sHHABrt5r_s'
revision_id = '1fe7397c17304d3ba4ea41f1eefc97fe'

# Authenticate
authenticator = SignavioAuthenticator(system_instance, tenant_id, user_name, pw)
auth_data = authenticator.authenticate()

print("Authenticated!")
cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
headers = {'Accept': 'application/json', 'x-signavio-id': auth_data['auth_token']}
diagram_url = system_instance + '/p/revision'

print(diagram_url)


# Fetch and save JSON diagram
json_url = (f'{diagram_url}/{revision_id}/json')
print(json_url)
json_request = requests.get(json_url, cookies=cookies, headers=headers)
print(json_request)
json_diagram = json_request.content
path = './diagram.json'
with open(path, 'w') as f:
    json.dump(json.loads(json_diagram), f)
# ISSUE: FIND OUT WHERE THE JSON FILE FOR THE DIAGRAM IS LOCATED
# Fetch and display PNG diagram
png_request = requests.get(f'{diagram_url}/{revision_id}/png', cookies=cookies, headers=headers)
display(Image(png_request.content))
