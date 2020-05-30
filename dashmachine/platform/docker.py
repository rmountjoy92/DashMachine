"""
##### Docker
Display information from Docker API. Informations can be displayed on a custom card or on an app card (e.g. Portainer App)
```ini
[variable_name]
platform = docker
prefix = http://
host = localhost
port = 2375
value_template = {{ value_template }}
```
> **Returns:** `value_template` as rendered string
| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | docker            |
| prefix          | No       | The prefix for the app's url.                                   | web prefix, e.g. http:// or https://              |
| host            | Yes      | Docker Host                                                     | url,ip            |
| port            | No       | Docker Port                                                     | port, usually 2375 (Insecure) or 2376 (TLS)              |
| api_version     | No       | Docker API version to use (Default : platform will try to find latest version)                                      | 1.40           |
| tls_mode        | No       | TLS verification mode, default is None                          | Server, Client, Both, None        |
| tls_ca          | No       | Requierd for tls_mode=Both or tls_mode=Server, default is None  | /path/to/ca, None |
| tls_cert        | No       | Requierd for tls_mode=Both or tls_mode=Client, default is None  | /path/to/cert, None |
| tls_key         | No       | Requierd for tls_mode=Both or tls_mode=Client, default is None  | /path/to/key, None|
| card_type       | No       | Set to Custom if you want to display informations in a custom card. Default is App | Custom, App|
| value_template  | Yes      | Jinja template for how the returned data from API is displayed. | jinja template    |
<br />
###### **Available fields for value_template**
* version
* max_api_version
* name
* containers
* containers_running
* containers_paused
* containers_stopped
* images
* driver
* cpu
* memory
* warnings
* error (for debug)
> **Working example (using un-encrypted connection, on Portainer card):**
>```ini
> [docker-endpoint-1]
> platform = docker
> prefix = http://
> host = 192.168.0.110
> port = 2375
> value_template = {{error}}<p style="text-align:right;text-transform:uppercase;font-size:14px;font-family: monospace;">{{name}}<br /><i style="position: relative; top: .2rem" class="material-icons md-18 theme-success-text" title="Running">fiber_manual_record</i>{{containers_running}}<i style="position: relative; top: .2rem" class="material-icons md-18 theme-warning-text" title="Paused">fiber_manual_record</i>{{containers_paused}}<i style="position: relative; top: .2rem" class="material-icons md-18 theme-failure-text" title="Stopped">fiber_manual_record</i>{{containers_stopped}}</p>
>
> [Portainer]
> prefix = http://
> url = 192.168.0.110:2375
> icon = static/images/apps/portainer.png
> sidebar_icon = static/images/apps/portainer.png
> description = Making Docker management easy
> open_in = this_tab
> data_sources = docker-endpoint-1
>```
>
>
> **Working example (using encrypted connection, on Portainer card):**
>```ini
> [docker-endpoint-2]
> platform = docker
> prefix = https://
> host = 192.168.0.110
> port = 2376
> tls_mode = Both
> tls_ca = /path/to/ca_file
> tls_cert = /path/to/cert_file
> tls_key = /path/to/key_file
> value_template = {{error}}<p style="text-align:right;text-transform:uppercase;font-size:14px;font-family: monospace;">{{name}}<br /><i style="position: relative; top: .2rem" class="material-icons md-18 theme-success-text" title="Running">fiber_manual_record</i>{{containers_running}}<i style="position: relative; top: .2rem" class="material-icons md-18 theme-warning-text" title="Paused">fiber_manual_record</i>{{containers_paused}}<i style="position: relative; top: .2rem" class="material-icons md-18 theme-failure-text" title="Stopped">fiber_manual_record</i>{{containers_stopped}}</p>
>
> [Portainer]
> prefix = http://
> url = 192.168.0.110:2375
> icon = static/images/apps/portainer.png
> sidebar_icon = static/images/apps/portainer.png
> description = Making Docker management easy
> open_in = this_tab
> data_sources = docker-endpoint-2
>```
>
>
> **Working example (using un-encrypted connection, on custom Docker card):**
>```ini
> [docker-endpoint-3]
> platform = docker
> prefix = http://
> host = 192.168.0.110
> port = 2375
> card_type = Custom
>
> [Docker]
> type = custom
> data_sources = docker-endpoint-3
>```
"""

import json
from flask import render_template_string
import requests
import re


class Docker(object):
    def __init__(
        self,
        method,
        prefix,
        host,
        port,
        api_version,
        card_type,
        tls_mode,
        tls_ca,
        tls_cert,
        tls_key,
    ):
        self.endpoint = None
        self.method = method
        self.prefix = prefix
        self.host = host
        self.port = port
        self.api_version = api_version
        self.card_type = card_type
        self.tls_mode = tls_mode
        self.tls_ca = tls_ca
        self.tls_key = tls_key
        self.tls_cert = tls_cert

        # Initialize results
        self.error = None
        self.version = "?"
        self.max_api_version = "?"
        self.name = "?"
        self.running = 0
        self.paused = 0
        self.stopped = 0
        self.images = 0
        self.driver = "?"
        self.cpu = "?"
        self.memory = "?"
        self.html_template = ""

    def check(self):
        port = "" if self.port == None else ":" + self.port

        if self.method.upper() == "GET":
            try:
                response = ""
                request = requests.get(
                    self.prefix + self.host + port + "/v999/info",
                    verify=self.tls_ca,
                    cert=(self.tls_cert, self.tls_key),
                    timeout=10,
                )
                response = request.text
                if "text/plain" in request.headers["content-type"]:
                    self.error = request.text
                    rawdata = None
                elif "application/json" in request.headers["content-type"]:
                    rawdata = request.json()
                else:
                    error = request
                    rawdata = None

            except Exception as e:
                rawdata = None
                self.error = f"{e}" + " " + response
                self.setHtml()

        if rawdata != None:
            if "message" in rawdata:
                regex = r"\bv?[0-9]+\.[0-9]+(?:\.[0-9]+)?\b"
                r = re.search(regex, rawdata["message"])
                self.max_api_version = r.group(0)
                self.api_version = (
                    self.api_version
                    if self.api_version != None
                    else self.max_api_version
                )
                self.endpoint = "/v" + self.api_version + "/"

    def getStatus(self):
        port = "" if self.port == None else ":" + self.port

        if self.method.upper() == "GET":
            try:
                rawdata = requests.get(
                    self.prefix + self.host + port + self.endpoint + "/info",
                    verify=self.tls_ca,
                    cert=(self.tls_cert, self.tls_key),
                    timeout=10,
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"
                self.setHtml()

        if rawdata != None:
            self.name = rawdata["Name"]
            self.containers = rawdata["Containers"]
            self.containers_running = rawdata["ContainersRunning"]
            self.containers_paused = rawdata["ContainersPaused"]
            self.containers_stopped = rawdata["ContainersStopped"]
            self.images = rawdata["Images"]
            self.warnings = rawdata["Warnings"]
            self.driver = rawdata["Driver"]
            self.cpu = rawdata["NCPU"]
            self.memory = self.formatSize(rawdata["MemTotal"])
            if self.card_type == "Custom":
                self.setHtml()

    def formatSize(self, size):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        power_labels = {0: "", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
        while size > power:
            size /= power
            n += 1
        return str(round(size, 1)) + " " + power_labels[n]

    def refresh(self):
        self.check()
        if self.error == None:
            self.error = ""
            self.getStatus()

    def setHtml(self):
        if self.error != None and self.error != "":
            self.html_template = """
            <div class="row">
                <div class="col s6">
                    <span class="mt-0 mb-0 theme-primary-text font-weight-700" style="font-size: 36px"><i class="material-icons md-18 theme-failure-text" title="Error">error</i></h3>
                </div>
                <div class="col s6 right-align">
                    <img height="48px" src="static/images/apps/docker.png" alt="Docker">
                </div>
            </div>
            <div class="row">
                <h6 class="font-weight-900 center theme-muted-text">Error</h6>
            </div>
            <div class="row center-align">
                <i class="material-icons-outlined">keyboard_arrow_down</i>
            </div>
            <div class="row center-align">
                <div class="col s12">
                    <div class="collection theme-muted-text">
                        <div class="collection-item">{{ error }}</div>
                    </div>
                </div>
            </div>
            """
        else:
            if self.tls_mode == None:
                img_tls = """
                        <i class="material-icons md-18 theme-warning-text" title="TLS disabled">lock_open</i>
                        """
            else:
                img_tls = """
                        <i class="material-icons md-18 theme-success-text" title="TLS enabled">lock</i>
                        """
            if len(self.warnings) > 0:
                img_warnings = """
                        <i class="material-icons md-18 theme-warning-text" title="{{warnings}}">warning</i>
                        """
            else:
                img_warnings = """
                        <i class="material-icons md-18 theme-muted2-text" title="No warnings">warning</i>
                        """
            self.html_template = (
                """
            <div class="row">
                <div class="col s6">
                    <span class="mt-0 mb-0 theme-primary-text font-weight-700" style="font-size: 36px">"""
                + img_tls
                + img_warnings
                + """</h3>
                </div>
                <div class="col s6 right-align">
                    <img height="48px" src="static/images/apps/docker.png" alt="Docker">
                </div>
            </div>
            <div class="row">
                <h6 class="font-weight-900 center theme-muted-text">{{name}}</h6>
            </div>
            <div class="row center-align">
                <i class="material-icons-outlined">keyboard_arrow_down</i>
            </div>
            <div class="row center-align">
                <div class="col s12">
                    <div class="collection theme-muted-text">
                        <div class="collection-item"><span class="font-weight-900">Containers: </span>{{ containers }}</div>
                        <div class="collection-item"><span class="font-weight-900">Running: </span>{{ containers_running }}</div>
                        <div class="collection-item"><span class="font-weight-900">Paused: </span>{{ containers_paused }}</div>
                        <div class="collection-item"><span class="font-weight-900">Stopped: </span>{{ containers_stopped }}</div>
                        <div class="collection-item"><span class="font-weight-900">Images: </span>{{ images }}</div>
                        <div class="collection-item"><span class="font-weight-900">Driver: </span>{{ driver }}</div>
                        <div class="collection-item"><span class="font-weight-900">CPU: </span>{{ cpu }}</div>
                        <div class="collection-item"><span class="font-weight-900">Memory: </span>{{ memory }}</div>
                    </div>
                </div>
            </div>
            """
            )

    def getHtml(self):
        return self.html_template


class Platform:
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
            self.port = 2375
        if not hasattr(self, "api_version"):
            self.api_version = None
        if not hasattr(self, "card_type"):
            self.card_type = "App"
        if not hasattr(self, "tls_ca"):
            self.tls_ca = None
        if not hasattr(self, "tls_cert"):
            self.tls_cert = None
        if not hasattr(self, "tls_key"):
            self.tls_key = None
        # Without TLS
        if not hasattr(self, "tls_mode"):
            self.tls_mode = None
            self.tls_ca = None
            self.tls_cert = None
            self.tls_key = None
        else:
            if self.tls_mode == "Both":
                if self.tls_ca == None or self.tls_cert == None or self.tls_key == None:
                    return "tls_mode set to Both, and missing tls_ca/tls_cert/tls_key"
            elif self.tls_mode == "Client":
                self.tls_ca = False
            elif self.tls_mode == "Server":
                self.tls_cert = ""
                self.tls_key = ""
            elif self.tls_mode == "None":
                self.tls_ca = None
                self.tls_cert = None
                self.tls_key = None

        self.docker = Docker(
            self.method,
            self.prefix,
            self.host,
            self.port,
            self.api_version,
            self.card_type,
            self.tls_mode,
            self.tls_ca,
            self.tls_cert,
            self.tls_key,
        )

    def process(self):
        if self.host == None:
            return "host missing"
        # TLS check
        if self.tls_mode == "Both":
            if self.tls_ca == None or self.tls_cert == None or self.tls_key == None:
                return "tls_mode set to Both, and missing tls_ca/tls_cert/tls_key"
        elif self.tls_mode == "Client":
            if self.tls_cert == None or self.tls_key == None:
                return "tls_mode set to Client, and missing tls_cert/tls_key"
        elif self.tls_mode == "Server":
            if self.tls_ca == None:
                return "tls_mode set to Server, and missing tls_ca"
        else:
            if self.tls_mode != None:
                return "Invalid tls_mode : " + self.tls_mode

        self.docker.refresh()

        if self.card_type == "Custom":
            return render_template_string(self.docker.getHtml(), **self.docker.__dict__)
        else:
            return render_template_string(self.value_template, **self.docker.__dict__)
