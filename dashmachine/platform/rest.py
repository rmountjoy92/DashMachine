"""

##### rest
Make a call on a REST API and display the results as a jinja formatted string.
```ini
[variable_name]
platform = rest
resource = https://your-website.com/api
value_template = {{value}}
method = post
authentication = basic
username = my_username
password = my_password
payload = {"var1": "hi", "var2": 1}
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | rest              |
| resource        | Yes      | Url of rest api resource.                                       | url               |
| value_template  | Yes      | Jinja template for how the returned data from api is displayed. | jinja template    |
| method          | No       | Method for the api call, default is GET                         | GET,POST          |
| authentication  | No       | Authentication for the api call, default is None                | None,basic,digest |
| username        | No       | Username to use for auth.                                       | string            |
| password        | No       | Password to use for auth.                                       | string            |
| payload         | No       | Payload for post request.                                       | json              |

> **Working example:**
>```ini
>[test]
>platform = rest
>resource = https://pokeapi.co/api/v2/pokemon
>value_template = Pokemon: {{value['count']}}
>
>[Pokemon]
>prefix = https://
>url = pokemon.com
>icon = static/images/apps/default.png
>description = Data sources example
>open_in = this_tab
>data_sources = test
>```

"""

import json
from requests import get, post
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from flask import render_template_string


class Platform:
    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
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
