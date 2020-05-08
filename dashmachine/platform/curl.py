import requests
from flask import render_template_string


class Platform:
    def docs(self):
        documentation = {
            "name": "curl",
            "author": "buoyantotter",
            "author_url": "https://github.com/buoyantotter",
            "version": 1.0,
            "description": "Curl an URL and show result",
            "example": """
```ini
[test]
platform = curl
resource = https://api.myip.com
value_template = My IP: {{value.ip}}
response_type = json
[MyIp.com]
prefix = https://
url = myip.com
icon = static/images/apps/default.png
description = Link to myip.com
open_in = new_tab
data_sources = test
```
            """,
            "returns": "`value_template` as rendered string",
            "returns_json_keys": ["value"],
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
                    "default": "curl",
                    "options": "curl",
                },
                {
                    "variable": "resource",
                    "description": "Url to curl",
                    "default": "https://example.com",
                    "options": "url",
                },
                {
                    "variable": "value_template",
                    "description": "Jinja template for how the returned data from api is displayed.",
                    "default": "{{value}}",
                    "options": "jinja template",
                },
                {
                    "variable": "response_type",
                    "description": "Response type. Use json if response is a JSON.",
                    "default": "plain",
                    "options": "plain,json",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        # set defaults for omitted options
        if not hasattr(self, "response_type"):
            self.response_type = "plain"

    def process(self):
        if self.response_type.lower() == "json":
            try:
                value = requests.get(self.resource).json()
                print(value)
            except Exception as e:
                value = f"{e}"
        else:
            try:
                value = requests.get(self.resource)
            except Exception as e:
                value = f"{e}"

        return render_template_string(self.value_template, value=value)
