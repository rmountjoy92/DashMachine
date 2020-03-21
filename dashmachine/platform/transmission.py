"""

##### Transmission
Display information from the Trasnmission API
```ini
[variable_name]
platform = transmission
host = localhost
port = 9091
user = {{ transmission Web UI username }}
password = {{ Transmission Web UI password }}
value_template = {{ value_template }}
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | transmission      |
| host            | Yes      | Host of Transmission Web UI                                     | host              |
| port            | Yes      | Port of Transmission Web UI                                     | port              |
| user            | No       | Username for Transmission Web UI                                | username          |
| password        | No       | Password for Transmission Web UI                                | password          |
| value_template  | Yes      | Jinja template for how the returned data from API is displayed. | jinja template    |

<br />
###### **Available fields for value_template**

* downloadSpeed
* uploadSpeed
* activeTorrentCount
* pausedTorrentCount
* torrentCount

> **Working example:**
>```ini
> [transmission-data]
> platform = transmission
> host = 192.168.1.30
> port = 9091
> user = admin
> password = password123
> value_template = 🔽 {{(downloadSpeed/1024/1024)|round(2)}} MB/s<br>🔼 {{(uploadSpeed/1024/1024)|round(2)}} MB/s<br><strong>Active:</strong> {{activeTorrentCount}}<br>
>
> [Transmission]
> prefix = http://
> url = 192.168.1.30:9091
> icon = static/images/apps/transmission.png
> description = A Fast, Easy, and Free BitTorrent Client
> open_in = new_tab
> data_sources = transmission-data
>```
"""

import json
from flask import render_template_string
import transmissionrpc


# from pprint import PrettyPrinter
# pp = PrettyPrinter()


class Platform:
    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "port"):
            self.port = 9091
        if not hasattr(self, "host"):
            self.host = "localhost"

        self.tc = transmissionrpc.Client(
            self.host, port=self.port, user=self.user, password=self.password
        )

    def process(self):

        torrents = len(self.tc.get_torrents())
        data = {}
        for key, field in self.tc.session_stats().__dict__["_fields"].items():
            data[key] = field.value
        # pp.pprint (data)

        value_template = render_template_string(self.value_template, **data)
        return value_template


# Testing
# test = Platform(host='192.168.1.19', user='', password='').process()
