"""

##### Plex Media Server
Connect to Plex Media Server and see current sessions details
```ini
[variable_name]
platform = plex
url = http://plex_host:plex_port
token = plex_token
value_template = {{ value_template }}
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | plex              |
| host            | Yes      | URL of Plex Media Server (include port, normally 32400)         | url               |
| token           | Yes      | X-Plex-Token (See [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) for how to find it.)                 | string            |
| value_template  | Yes      | Jinja template for how the returned data from API is displayed. | jinja template    |

<br />
###### **Available fields for value_template**

* sessions
* transcodes
* libraries

> **Example:**
>```ini
>[plex]
>platform = plex
>host = http://plex.example.com:32400
>token = abcde_fghi_jklmnopqr
>value_template = Sessions: {{sessions}}<br />Transcodes: {{transcodes}}
>
>[Plex]
>prefix = http://
>url = plex.example.com:32400
>icon = static/images/apps/plex.png
>description = Plex data sources example
>open_in = this_tab
>data_sources = plex
>```

"""

import json
import requests
from flask import render_template_string

json_header = {"Accept": "application/json"}


class Plex(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def refresh(self):
        if self.token != None:
            sessions = requests.get(
                self.url
                + "/status/sessions?X-Plex-Token="
                + self.token, headers=json_header).json()

            self.sessions = sessions["MediaContainer"]["size"]

            transcodes = requests.get(
                self.url
                + "/transcode/sessions?X-Plex-Token="
                + self.token, headers=json_header).json()

            self.transcodes = transcodes["MediaContainer"]["size"]

            libraries = requests.get(
                self.url
                + "/library/sections?X-Plex-Token="
                + self.token, headers=json_header).json()

            self.libraries = libraries["MediaContainer"]["size"]


class Platform:
    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "token"):
            print("Please add a token\nSee https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/ to find it.")
            exit(1)
        else:
            self.plex = Plex(self.host, self.token)

    def process(self):
        self.plex.refresh()
        value_template = render_template_string(
            self.value_template, **self.plex.__dict__
        )
        return value_template
