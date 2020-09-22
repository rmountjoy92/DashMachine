"""

##### Octoprint
Display information from octoprint.
```ini
[variable_name]
platform = octoprint
resource = http://octopi.local
value_template = 
api_key = 
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | octoprint         |
| resource        | Yes      | Url of your octoprint instance                                  | url               |
| value_template  | Yes      | Jinja template for how the returned data from api is displayed. | jinja template    |
| api_key         | Yes      | API key to use for auth.                                        | string            |

> **Working example:**
>```
>[octoprint]
>platform = octoprint
>resource = http://octopi.local
>api_key = ABC123MYAPIKEY
>value_template = State: {{ state }} {% if state == "Printing" %} ({{completion|int}}%){% endif %}
>
>[Octoprint]
>prefix = http://
>url = octopi.local
>icon = static/images/icons/octoprint.png
>sidebar_icon = static/images/icons/octoprint.png
>description = Manage 3D printer
>open_in = new_tab
>data_sources = octoprint
>```

"""

from flask import render_template_string
import requests

def flatten_dict(d, r=None):
    if r is None:
        r = {}
    for k, v in d.items():
        r[k] = v
        if type(v) == dict:
            flatten_dict(v, r)
    return r


class Platform:
    JOB_PATH = "/api/job"

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "resource"):
            self.resource = "http://octopi.local"

        if not hasattr(self, "api_key"):
            self.api_key = ""

        self.session = requests.Session()

    def process(self):
        job = self.get_current_job()
        value_template = render_template_string(self.value_template, **flatten_dict(job))
        return value_template

    def get_current_job(self):
        return self.get(self.JOB_PATH).json()

    def request(self, verb, path, json={}):
        headers = {"X-Api-Key": self.api_key}
        return self.session.request(verb, self.resource + path, headers=headers, json=json)

    def get(self, path):
        return self.request("GET", path)

