import json
from requests import get, post
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from flask import render_template_string


class Platform:
    def docs(self):
        documentation = {
            "name": "rest",
            "author": "RMountjoy",
            "author_url": "https://github.com/rmountjoy92",
            "version": 1.0,
            "description": "Make a call on a REST API and display the results as a jinja formatted string.",
            "returns": "`value_template` as rendered string",
            "returns_json_keys": ["value"],
            "example": """
```ini
[test]
platform = rest
resource = https://pokeapi.co/api/v2/pokemon
value_template = Pokemon: {{value['count']}}

[Pokemon]
prefix = https://
url = pokemon.com
icon = static/images/apps/default.png
description = Data sources example
open_in = this_tab
data_sources = test
```
            """,
            "variables": [
                {
                    "variable": "[variable_name]",
                    "description": "Name for the data source.",
                    "default": "None, entry is required",
                    "options": ".ini header",
                },
                {
                    "variable": "platform",
                    "description": "Name of the platform.",
                    "default": "rest",
                    "options": "rest",
                },
                {
                    "variable": "resource",
                    "description": "Url of rest api resource.",
                    "default": "",
                    "options": "url",
                },
                {
                    "variable": "value_template",
                    "description": "Jinja template for how the returned data from api is displayed.",
                    "default": "{{value}}",
                    "options": "jinja template",
                },
                {
                    "variable": "method",
                    "description": "Method for the api call",
                    "default": "GET",
                    "options": "GET,POST",
                },
                {
                    "variable": "authentication",
                    "description": "Authentication for the api call",
                    "default": "",
                    "options": "None,basic,digest",
                },
                {
                    "variable": "username",
                    "description": "Username to use for auth.",
                    "default": "",
                    "options": "string",
                },
                {
                    "variable": "password",
                    "description": "Password to use for auth.",
                    "default": "",
                    "options": "string",
                },
                {
                    "variable": "payload",
                    "description": "Payload for post request.",
                    "default": "",
                    "options": "json",
                },
                {
                    "variable": "headers",
                    "description": "Custom headers for get or post",
                    "default": "",
                    "options": "json",
                },
                {
                    "variable": "verify",
                    "description": "Turn TLS verification on or off",
                    "default": "True",
                    "options": "True, False",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            if key == "headers":
                value = json.loads(value)
            self.__dict__[key] = value

        # set defaults for omitted options
        if not hasattr(self, "value_template"):
            self.method = "{{value}}"
        if not hasattr(self, "method"):
            self.method = "GET"
        if not hasattr(self, "authentication"):
            self.authentication = None
        if not hasattr(self, "headers"):
            self.headers = None
        if not hasattr(self, "verify"):
            self.verify = True

    def process(self):
        if self.authentication:
            if self.authentication.lower() == "digest":
                auth = HTTPDigestAuth(self.username, self.password)
            else:
                auth = HTTPBasicAuth(self.username, self.password)
        else:
            auth = None

        verify = False if str(self.verify).lower() == "false" else True

        if self.method.upper() == "GET":
            try:
                value = get(
                    self.resource, auth=auth, headers=self.headers, verify=verify
                ).json()
            except Exception as e:
                value = f"{e}"

        elif self.method.upper() == "POST":
            payload = json.loads(self.payload.replace("'", '"'))
            value = post(
                self.resource,
                data=payload,
                auth=auth,
                headers=self.headers,
                verify=verify,
            )
        value_template = render_template_string(self.value_template, value=value)
        return value_template
