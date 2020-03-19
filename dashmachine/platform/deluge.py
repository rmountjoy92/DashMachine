"""

##### deluge
Display information from Deluge web ui.
```ini
[variable_name]
platform = deluge
resource = https://deluge.example.com:8112/json
value_template = ↓{{download_rate|filesizeformat}}/s ↑{{upload_rate|filesizeformat}}/s
password = MySecretPassword
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | rest              |
| resource        | Yes      | Url of your deluge instance + '/json'                           | url               |
| value_template  | Yes      | Jinja template for how the returned data from api is displayed. | jinja template    |
| password        | No       | Password to use for auth.                                       | string            |

> **Working example:**
>```
>[deluge]
>platform = deluge
>resource = https://deluge.example.com:8112/json
>value_template = ↓{{download_rate|filesizeformat}}/s ↑{{upload_rate|filesizeformat}}/s
>password = MySecretPassword
>
>[Deluge]
>prefix = https://
>url = https://deluge.example.com:8112
>icon = static/images/apps/deluge.png
>sidebar_icon = static/images/apps/deluge.png
>description = Deluge is a lightweight, Free Software, cross-platform BitTorrent client
>open_in = iframe
>data_sources = deluge
>```

"""

from flask import render_template_string
import requests


class Platform:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "resource"):
            self.resource = "http://localhost/json"

        if not hasattr(self, "password"):
            self.password = ""

        self.id = 1
        self.session = requests.Session()
        self._api_call("auth.login", [self.password])
        self.password = None  # Discard password, no longer needed.

    def _api_call(self, method, params=[]):
        json = {"id": self.id, "method": method, "params": params}
        return self.session.post(self.resource, json=json)

    def process(self):
        r = self._api_call("web.update_ui", ["download_rate", "upload_rate"])
        json = r.json()
        data = {}
        for key, field in json["result"]["stats"].items():
            data[key] = field

        value_template = render_template_string(self.value_template, **data)
        return value_template
