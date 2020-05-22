"""

##### Healthchecks
Display information from Healthchecks API
```ini
[variable_name]
platform = healthchecks
prefix = http://
host = localhost
port = 8080
api_key = {{ Healthchecks project API Key }}
project = {{ Healthchecks project name }}
verify = true
value_template = {{ value_template }}
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | healthchecks      |
| prefix          | No       | The prefix for the app's url.                                   | web prefix, e.g. http:// or https://              |
| host            | Yes      | Healthchecks Host                                               | url,ip            |
| port            | No       | Healthchecks Port                                               | port              |
| api_key         | Yes      | ApiKey                                                          | api key           |
| project         | No       | Healthchecks project name                                       | project           |
| verify          | No       | Turn TLS verification on or off, default is true                | true,false        |
| value_template  | Yes      | Jinja template for how the returned data from API is displayed. | jinja template    |

<br />
###### **Available fields for value_template**

* status
* count_checks
* count_up
* count_down
* count_grace
* count_paused
* error (for debug)

> **Working example:**
>```ini
> [healthchecks-data]
> platform = healthchecks
> prefix = http://
> host = 192.168.0.110
> port = 8080
> api_key = {{ API Key }}
> project = {{ Project name }}
> verify = False
> value_template = {{error}}<p style="text-align:right;text-transform:uppercase;font-size:14px;font-family: monospace;"><i style="position: relative; top: .2rem" class="material-icons md-18 theme-success-text" title="Up">fiber_manual_record</i>{{count_up}}<i style="position: relative; top: .2rem" class="material-icons md-18 theme-warning-text" title="Grace">fiber_manual_record</i>{{count_grace}}<i style="position: relative; top: .2rem" class="material-icons md-18 theme-failure-text" title="Down">fiber_manual_record</i>{{count_down}}</p>
>
> [Healthchecks]
> prefix = http://
> url  = 192.168.0.110
> icon = static/images/apps/healthchecks.png
> description = Healthchecks is a watchdog for your cron jobs. It's a web server that listens for pings from your cron jobs, plus a web interface.
> open_in = this_tab
> data_sources = healthchecks-data
>```

"""

import json
from flask import render_template_string
import requests

class Healthchecks(object):

    def __init__(self,method, prefix, host, port, api_key, project, verify):
        self.endpoint = "/api/v1/checks/"
        self.method = method
        self.prefix = prefix
        self.host = host
        self.port = port
        self.api_key = api_key
        self.project = project
        self.verify = verify

        # Initialize results
        self.error = None
        self.status = ""
        self.count_checks = 0
        self.count_up = 0
        self.count_down = 0
        self.count_grace = 0
        self.count_paused = 0

    def check(self):
        verify = False if str(self.verify).lower() == "false" or str(self.prefix).lower() == "http://" else True
        headers = {'X-Api-Key': self.api_key}
        port = '' if self.port == None else ':' + self.port

        if self.method.upper() == "GET":
            try:
                rawdata = requests.get(
                    self.prefix
                    + self.host
                    + port
                    + self.endpoint
                    , headers=headers
                    , verify=verify
                    , timeout=10
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            if 'error' in rawdata:
                self.error = rawdata['error']
            

    def getChecks(self):        
        verify = False if str(self.verify).lower() == "false" or str(self.prefix).lower() == "http://" else True
        headers = {'X-Api-Key': self.api_key}
        port = '' if self.port == None else ':' + self.port

        if self.method.upper() == "GET":
            try:
                rawdata = requests.get(
                    self.prefix
                    + self.host
                    + port
                    + self.endpoint
                    , headers=headers
                    , verify=verify
                    , timeout=10
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            for check in rawdata['checks']:
                self.count_checks += 1
                if check['status'] == "up":
                    self.count_up += 1
                if check['status'] == "down":
                    self.count_down += 1
                if check['status'] == "grace":
                    self.count_grace += 1
                if check['status'] == "paused":
                    self.count_paused += 1

            if self.count_down > 0:
                self.status = "down"
            if self.count_down == 0 and self.count_grace > 0:
                self.status = "grace"
            if self.count_down == 0 and self.count_grace == 0:
                self.status = "up"

    def refresh(self):
        self.check()
        if self.error == None:
            self.error = ''
            self.getChecks()

class Platform:
    def __init__(self,*args,**kwargs):
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
        if not hasattr(self, "project"):
            self.project = None
        if not hasattr(self, "verify"):
            self.verify = True

        self.healthchecks = Healthchecks(self.method, self.prefix, self.host, self.port, self.api_key, self.project, self.verify)

    def process(self):
        if self.api_key == None:
            return "api_key missing"
        if self.host == None:
            return "host missing"

        self.healthchecks.refresh()
        value_template = render_template_string(
            self.value_template, **self.healthchecks.__dict__
        )
        return value_template
