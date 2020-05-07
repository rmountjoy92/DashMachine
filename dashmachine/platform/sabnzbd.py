from flask import render_template_string
import requests


class Sabnzbd(object):
    # Takes the ip address of Sabnzbd
    def __init__(self, ip_address, port, api_key):
        self.ip_address = ip_address
        self.port = port
        self.api_key = api_key

    def refresh(self):
        if self.api_key != None:
            rawdata = requests.get(
                "http://"
                + self.ip_address
                + ":"
                + self.port
                + "/api?"
                + "apikey="
                + self.api_key
                + "&mode=queue"
                + "&output=json"
            ).json()

        queue = rawdata["queue"]
        self.status = queue["status"]
        self.no_of_slots = queue["noofslots_total"]
        self.speed = queue["speed"]
        self.size = queue["size"]
        self.disk_free = queue["diskspace1_norm"]
        self.eta = queue["eta"]
        self.mb_left = queue["mbleft"]
        self.time_left = queue["timeleft"]


class Platform:
    def docs(self):
        documentation = {
            "name": "sabnzbd",
            "author": "rxmii4269",
            "author_url": "https://github.com/rxmii4269",
            "version": 1.0,
            "description": "Display information from the SABnzbd API",
            "example": """
```ini
[sabnzbd-data]
platform = sabnzbd
host = 192.168.x.x
port = 8080
api_key = my_api_key
value_template = Status:{{status}}<br>⬇ {{speed}}<br>Size: {{size}}<br>

[Sabnzbd]
prefix = http://
url  = 192.168.1.32:8080
icon = static/images/apps/sabnzbd.png
description = SABnzbd is a multi-platform binary newsgroup downloader. The program works in the background and simplifies the downloading verifying and extracting of files from Usenet.
open_in = iframe
data_sources = sabnzbd-data
```
            """,
            "returns": "`value_template` as rendered string",
            "returns_json_keys": [
                "status",
                "no_of_slots",
                "speed",
                "size",
                "disk_free",
                "eta",
                "mb_left",
                "time_left",
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
                    "default": "sabnzbd",
                    "options": "sabnzbd",
                },
                {
                    "variable": "host",
                    "description": "Host of Sabnzbd",
                    "default": "192.168.x.x",
                    "options": "host",
                },
                {
                    "variable": "port",
                    "description": "Port of Sabnzbd",
                    "default": "8080",
                    "options": "port",
                },
                {
                    "variable": "api_key",
                    "description": "Api key for the Sabnzbd",
                    "default": "my_api_key",
                    "options": "api key",
                },
                {
                    "variable": "value_template",
                    "description": "Jinja template for how the returned data from API is displayed.",
                    "default": "Status:{{status}}<br>⬇ {{speed}}<br>Size: {{size}}<br>",
                    "options": "jinja template",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def pre_process(self):
        self.sabnzbd = Sabnzbd(self.host, self.port, self.api_key)
        return self

    def process(self):
        self = self.pre_process(self)
        self.sabnzbd.refresh()
        value_template = render_template_string(
            self.value_template, **self.sabnzbd.__dict__
        )
        return value_template
