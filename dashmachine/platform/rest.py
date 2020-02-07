import json
from requests import get, post
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from flask import render_template_string


class Platform:
    def __init__(self, data_source, data_source_args):
        # parse the user's options from the config entries
        for key, value in data_source_args.items():
            self.__dict__[key] = value

        # set defaults for omitted options
        if not hasattr(self, "method"):
            self.method = "GET"
        if not hasattr(self, "authentication"):
            self.authentication = None

    def process(self):
        if self.method.upper() == "GET":
            try:
                value = get(self.resource).json()
            except Exception as e:
                value = f"{e}"

        elif self.method.upper() == "POST":
            if self.authentication:
                if self.authentication.lower() == "digest":
                    auth = HTTPDigestAuth(self.username, self.password)
                else:
                    auth = HTTPBasicAuth(self.username, self.password)
            else:
                auth = None

            payload = json.loads(self.payload.replace("'", '"'))
            value = post(self.resource, data=payload, auth=auth)
        value_template = render_template_string(self.value_template, value=value)
        return value_template
