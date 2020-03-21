"""

##### curl
Curl an URL and show result
```ini
[variable_name]
platform = curl
resource = https://example.com
value_template = {{value}}
response_type = json
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| plaform         | Yes      | Name of the platform.                                           | curl              |
| resource        | Yes      | Url to curl                                                     | url               |
| value_template  | Yes      | Jinja template for how the returned data from api is displayed. | jinja template    |
| response_type   | No       | Response type. Use json if response is a JSON. Default is plain.| plain,json        |

> **Working example:**
>```ini
>[test]
>platform = curl
>resource = https://api.myip.com
>value_template = My IP: {{value.ip}}
response_type = json
>
>[MyIp.com]
>prefix = https://
>url = myip.com
>icon = static/images/apps/default.png
>description = Link to myip.com
>open_in = new_tab
>data_sources = test
>```
"""

import requests
from flask import render_template_string


class Platform:
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
