"""

##### SABnzbd
Display information from the SABnzbd API
```ini
[variable_name]
platform = sabnzbd
host = localhost
port = 8080
api_key = my_api_key
value_template = {{ value_template }}
``` 
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | sabnzbd           |
| host            | Yes      | Host of Sabnzbd                                                 | host              |
| port            | Yes      | Port of Sabnzbd                                                 | port              |
| api_key         | Yes      | Api key for the Sabnzbd                                         | api key           |
| value_template  | Yes      | Jinja template for how the returned data from API is displayed. | jinja template    |

<br />
###### **Available fields for value_template**

* status
* no_of_slots
* speed
* size
* disk_free
* eta
* mb_left
* time_left

> **Working example:**
>```ini
> [sabnzbd-data]
> platform = sabnzbd
> host = 192.168.1.32
> port = 8080
> api_key = {{ API Key}}
> value_template = Status:{{status}}<br>⬇ {{speed}}<br>Size: {{size}}<br>
>
> [Sabnzbd]
> prefix = http://
> url  = 192.168.1.32:8080
> icon = static/images/apps/sabnzbd.png
> description = SABnzbd is a multi-platform binary newsgroup downloader. The program works in the background and simplifies the downloading verifying and extracting of files from Usenet.
> open_in = iframe
> data_sources = sabnzbd-data
>```
"""

import json
from flask import render_template_string
import requests



class Sabnzbd(object):
    # Takes the ip address of Sabnzbd
    def __init__(self,ip_address,port,api_key):
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
    def __init__(self,*args,**kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.sabnzbd = Sabnzbd(self.host, self.port, self.api_key)

    def process(self):
        self.sabnzbd.refresh()
        value_template = render_template_string(
            self.value_template, **self.sabnzbd.__dict__
        )
        return value_template