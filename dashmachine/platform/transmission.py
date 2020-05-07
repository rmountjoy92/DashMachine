from flask import render_template_string
import transmissionrpc


class Platform:
    def docs(self):
        documentation = {
            "name": "transmission",
            "author": "Nixellion",
            "author_url": "https://github.com/Nixellion",
            "version": 1.0,
            "description": "Display information from the Trasnmission API",
            "example": """
```ini
[transmission-data]
platform = transmission
host = localhost
port = 9091
user = my_username
password = my_password
value_template = 🔽 {{(downloadSpeed/1024/1024)|round(2)}} MB/s<br>🔼 {{(uploadSpeed/1024/1024)|round(2)}} MB/s<br><strong>Active:</strong> {{activeTorrentCount}}<br>

[Transmission]
prefix = http://
url = 192.168.1.30:9091
icon = static/images/apps/transmission.png
description = A Fast, Easy, and Free BitTorrent Client
open_in = new_tab
data_sources = transmission-data
```
            """,
            "returns": "`value_template` as rendered string",
            "returns_json_keys": [
                "downloadSpeed",
                "uploadSpeed",
                "activeTorrentCount",
                "pausedTorrentCount",
                "torrentCount",
            ],
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
                    "default": "transmission",
                    "options": "transmission",
                },
                {
                    "variable": "host",
                    "description": "Host of Transmission Web UI ",
                    "default": "localhost",
                    "options": "host",
                },
                {
                    "variable": "port",
                    "description": "Port of Transmission Web UI  ",
                    "default": "9091",
                    "options": "port",
                },
                {
                    "variable": "user",
                    "description": "Username for Transmission Web UI ",
                    "default": "my_username",
                    "options": "string",
                },
                {
                    "variable": "password",
                    "description": "Password for Transmission Web UI.",
                    "default": "my_password",
                    "options": "string",
                },
                {
                    "variable": "value_template",
                    "description": "Jinja template for how the returned data from API is displayed.",
                    "default": "{{(downloadSpeed/1024/1024)|round(2)}} MB/s<br>🔼 {{(uploadSpeed/1024/1024)|round(2)}} MB/s<br><strong>Active:</strong> {{activeTorrentCount}}<br>",
                    "options": "jinja template",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "port"):
            self.port = 9091
        if not hasattr(self, "host"):
            self.host = "localhost"

    def process(self):
        self.tc = transmissionrpc.Client(
            self.host, port=self.port, user=self.user, password=self.password
        )

        torrents = len(self.tc.get_torrents())
        data = {}
        for key, field in self.tc.session_stats().__dict__["_fields"].items():
            data[key] = field.value
        # pp.pprint (data)

        value_template = render_template_string(self.value_template, **data)
        return value_template


# Testing
# test = Platform(host='192.168.1.19', user='', password='').process()
