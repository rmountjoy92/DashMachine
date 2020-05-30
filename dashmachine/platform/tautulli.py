from flask import render_template_string
import requests


class Tautulli(object):
    def __init__(self, method, prefix, host, port, api_key, verify):
        self.endpoint = "/api/v2"
        self.method = method
        self.prefix = prefix
        self.host = host
        self.port = port
        self.api_key = api_key
        self.verify = verify

        # Initialize results
        self.error = None
        self.update_available = ""
        self.update_message = ""
        self.stream_count = ""

    def check(self):
        verify = (
            False
            if str(self.verify).lower() == "false"
            or str(self.prefix).lower() == "http://"
            else True
        )
        headers = {"X-Api-Key": self.api_key}
        port = "" if self.port == None else ":" + self.port

        if self.method.upper() == "GET":
            try:
                rawdata = requests.get(
                    self.prefix
                    + self.host
                    + port
                    + self.endpoint
                    + "?apikey="
                    + self.api_key
                    + "&cmd="
                    + "update_check",
                    verify=verify,
                    timeout=10,
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            if "response" in rawdata and rawdata["response"]["result"] == "error":
                self.error = rawdata["response"]["message"]

    def getUpdate(self):
        verify = (
            False
            if str(self.verify).lower() == "false"
            or str(self.prefix).lower() == "http://"
            else True
        )
        port = "" if self.port == None else ":" + self.port

        if self.method.upper() == "GET":
            try:
                rawdata = requests.get(
                    self.prefix
                    + self.host
                    + port
                    + self.endpoint
                    + "?apikey="
                    + self.api_key
                    + "&cmd="
                    + "update_check",
                    verify=verify,
                    timeout=10,
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            self.update_message = rawdata["response"]["message"]
            self.update_available = rawdata["response"]["data"]["update"]

    def getActivity(self):
        verify = (
            False
            if str(self.verify).lower() == "false"
            or str(self.prefix).lower() == "http://"
            else True
        )
        port = "" if self.port == None else ":" + self.port

        if self.method.upper() == "GET":
            try:
                rawdata = requests.get(
                    self.prefix
                    + self.host
                    + port
                    + self.endpoint
                    + "?apikey="
                    + self.api_key
                    + "&cmd="
                    + "get_activity",
                    verify=verify,
                    timeout=10,
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            self.stream_count = rawdata["response"]["data"]["stream_count"]
            self.stream_count_direct_play = rawdata["response"]["data"][
                "stream_count_direct_play"
            ]
            self.stream_count_direct_stream = rawdata["response"]["data"][
                "stream_count_direct_stream"
            ]
            self.stream_count_transcode = rawdata["response"]["data"][
                "stream_count_transcode"
            ]
            self.total_bandwidth = rawdata["response"]["data"]["total_bandwidth"]
            self.wan_bandwidth = rawdata["response"]["data"]["wan_bandwidth"]

    def refresh(self):
        self.check()
        if self.error == None:
            self.error = ""
            self.getUpdate()
            self.getActivity()


class Platform:
    def docs(self):
        documentation = {
            "name": "tautulli",
            "author": "Thlb",
            "author_url": "https://github.com/Thlb",
            "version": 1.0,
            "description": "Display information from Tautulli API",
            "returns": "`value_template` as rendered string",
            "returns_json_keys": [
                "stream_count",
                "stream_count_direct_play",
                "stream_count_direct_stream",
                "stream_count_transcode",
                "total_bandwidth",
                "wan_bandwidth",
                "update_available",
                "update_message",
                "error (for debug)",
            ],
            "example": """
```ini
[tautulli-data]
platform = tautulli
prefix = http://
host = 192.168.0.110
port = 8181
api_key = myApiKey
verify = False
value_template = {{error}}Active sessions : {{stream_count}}

[Tautulli]
prefix = http://
url = 192.168.0.110:8181
icon = static/images/apps/tautulli.png
sidebar_icon = static/images/apps/tautulli.png
description = A Python based monitoring and tracking tool for Plex Media Server
open_in = this_tab
data_sources = tautulli-data
```
            """,
            "variables": [
                {
                    "variable": "[variable_name]",
                    "description": "Name for the data source.",
                    "default": "None, entry is required",
                    "options": ".ini header",
                },
                {
                    "variable": "platform",
                    "description": "Name of the platform.",
                    "default": "tautulli",
                    "options": "tautulli",
                },
                {
                    "variable": "prefix",
                    "description": "The prefix for the app's url.",
                    "default": "",
                    "options": "web prefix, e.g. http:// or https://",
                },
                {
                    "variable": "host",
                    "description": "Tautulli Host",
                    "default": "",
                    "options": "url,ip",
                },
                {
                    "variable": "port",
                    "description": "Tautulli Port",
                    "default": "",
                    "options": "port",
                },
                {
                    "variable": "api_key",
                    "description": "ApiKey",
                    "default": "",
                    "options": "api key",
                },
                {
                    "variable": "verify",
                    "description": "Turn TLS verification on or off, default is true",
                    "default": "",
                    "options": "true,false",
                },
                {
                    "variable": "value_template",
                    "description": "Jinja template for how the returned data from API is displayed.",
                    "default": "",
                    "options": "jinja template",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        # set defaults for omitted options
        if not hasattr(self, "method"):
            self.method = "GET"
        if not hasattr(self, "prefix"):
            self.prefix = "http://"
        if not hasattr(self, "host"):
            self.host = None
        if not hasattr(self, "port"):
            self.port = None
        if not hasattr(self, "api_key"):
            self.api_key = None
        if not hasattr(self, "verify"):
            self.verify = True

        self.tautulli = Tautulli(
            self.method, self.prefix, self.host, self.port, self.api_key, self.verify
        )

    def process(self):
        if self.api_key == None:
            return "api_key missing"
        if self.host == None:
            return "host missing"

        self.tautulli.refresh()
        value_template = render_template_string(
            self.value_template, **self.tautulli.__dict__
        )
        return value_template
