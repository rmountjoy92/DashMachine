"""

##### Sonarr
Display information from Sonarr API
```ini
[variable_name]
platform = sonarr
prefix = http://
host = localhost
port = 8989
api_key = {{ Sonarr API Key }}
verify = true
value_template = {{ value_template }}
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | sonarr            |
| prefix          | No       | The prefix for the app's url.                                   | web prefix, e.g. http:// or https://              |
| host            | Yes      | Sonarr Host                                                     | url,ip            |
| port            | No       | Sonarr Port                                                     | port              |
| api_key         | Yes      | ApiKey                                                          | api key           |
| verify          | No       | Turn TLS verification on or off, default is true                | true,false        |
| value_template  | Yes      | Jinja template for how the returned data from API is displayed. | jinja template    |

<br />
###### **Available fields for value_template**

* version
* wanted_missing
* queue
* diskspace[x]['path']
* diskspace[x]['total']
* diskspace[x]['used']
* diskspace[x]['free']
* error (for debug)

> **Working example:**
>```ini
> [sonarr-data]
> platform = sonarr
> prefix = http://
> host = 192.168.0.110
> port = 8989
> api_key = {{ API Key }}
> verify = False
> value_template = {{error}}Missing : {{wanted_missing}}<br />Queue : {{queue}} <br />Free ({{diskspace[0]['path']}}) : {{diskspace[0]['free']}}
>
> [Sonarr]
> prefix = http://
> url = 192.168.0.110:8989
> icon = static/images/apps/sonarr.png
> sidebar_icon = static/images/apps/sonarr.png
> description = Smart PVR for newsgroup and bittorrent users
> open_in = this_tab
> data_sources = sonarr-data
>```
"""

import json
from flask import render_template_string
import requests

class Sonarr(object):

    def __init__(self,method, prefix, host, port, api_key, verify):
        self.endpoint = "/api"
        self.method = method
        self.prefix = prefix
        self.host = host
        self.port = port
        self.api_key = api_key
        self.verify = verify

        # Initialize results
        self.error = None
        self.version = '?'
        self.wanted_missing = 0
        self.queue = 0
        self.diskspace = [{'path':'','total':'','free':'','used':''},{'path':'','total':'','free':'','used':''}]

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
                    + "/system/status"
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

    def getVersion(self):
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
                    + "/system/status"
                    , headers=headers
                    , verify=verify
                    , timeout=10
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            self.version = rawdata['version']

    def getWanted(self):
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
                    + "/wanted/missing/"
                    , headers=headers
                    , verify=verify
                    , timeout=10
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            self.wanted_missing = rawdata['totalRecords']
    
    def getQueue(self):
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
                    + "/queue"
                    , headers=headers
                    , verify=verify
                    , timeout=10
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            self.queue = len(rawdata)

    def getDiskspace(self):
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
                    + "/diskspace"
                    , headers=headers
                    , verify=verify
                    , timeout=10
                ).json()
            except Exception as e:
                rawdata = None
                self.error = f"{e}"

        if rawdata != None:
            self.diskspace = rawdata
            for item in self.diskspace:
                item['used'] = self.formatSize(item['totalSpace'] - item['freeSpace'])
                item['total'] = self.formatSize(item['totalSpace'])
                item['free'] = self.formatSize(item['freeSpace'])
                item.pop('totalSpace', None)
                item.pop('freeSpace', None)

    def formatSize(self, size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size > power:
            size /= power
            n += 1
        return str(round(size,1)) + ' ' + power_labels[n]
        
    def refresh(self):
        self.check()
        if self.error == None:
            self.error = ''
            self.getVersion()
            self.getWanted()
            self.getQueue()
            self.getDiskspace()

       
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
        if not hasattr(self, "verify"):
            self.verify = True

        self.sonarr = Sonarr(self.method, self.prefix, self.host, self.port, self.api_key, self.verify)

    def process(self):
        if self.api_key == None:
            return "api_key missing"
        if self.host == None:
            return "host missing"

        self.sonarr.refresh()
        value_template = render_template_string(
            self.value_template, **self.sonarr.__dict__
        )
        return value_template
