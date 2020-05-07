from flask import render_template_string
import requests


class Platform:
    def docs(self):
        documentation = {
            "name": "deluge",
            "author": "Azelphur",
            "author_url": "https://github.com/Azelphur",
            "version": 1.0,
            "description": "Display information from Deluge web ui.",
            "example": """
```ini
[deluge]
platform = deluge
resource = https://deluge.example.com:8112/json
value_template = ↓{{download_rate|filesizeformat}}/s ↑{{upload_rate|filesizeformat}}/s
password = MySecretPassword

[Deluge]
prefix = https://
url = https://deluge.example.com:8112
icon = static/images/apps/deluge.png
sidebar_icon = static/images/apps/deluge.png
description = Deluge is a lightweight, Free Software, cross-platform BitTorrent client
open_in = iframe
data_sources = deluge
```
            """,
            "returns": "`value_template` as rendered string",
            "variables": [
                {
                    "variable": "[variable_name]",
                    "description": "Name for the data source.",
                    "default": "",
                    "options": ".ini header",
                },
                {
                    "variable": "platform",
                    "description": "Name of the platform.",
                    "default": "deluge",
                    "options": "deluge",
                },
                {
                    "variable": "resource",
                    "description": "Url of your deluge instance + '/json'",
                    "default": "https://deluge.example.com:8112/json",
                    "options": "url",
                },
                {
                    "variable": "value_template",
                    "description": "Jinja template for how the returned data from api is displayed.",
                    "default": "↓{{download_rate|filesizeformat}}/s ↑{{upload_rate|filesizeformat}}/s",
                    "options": "jinja template",
                },
                {
                    "variable": "password",
                    "description": "Password to use for auth.",
                    "default": "",
                    "options": "string",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "resource"):
            self.resource = "http://localhost/json"

        if not hasattr(self, "password"):
            self.password = ""

    def pre_process(self):
        self.id = 1
        self.session = requests.Session()
        self._api_call("auth.login", [self.password])
        self.password = None  # Discard password, no longer needed.
        return self

    def _api_call(self, method, params=[]):
        json = {"id": self.id, "method": method, "params": params}
        return self.session.post(self.resource, json=json)

    def process(self):
        self = self.pre_process()
        r = self._api_call("web.update_ui", ["download_rate", "upload_rate"])
        json = r.json()
        data = {}
        for key, field in json["result"]["stats"].items():
            data[key] = field

        value_template = render_template_string(self.value_template, **data)
        return value_template
