"""

##### http_status
Make a http call on a given URL and display if the service is online.
```ini
[variable_name]
platform = http_status
resource = https://your-website.com/api
method = get
authentication = basic
username = my_username
password = my_password
headers = {"Content-Type": "application/json"}
return_codes = 2xx,3xx
```
> **Returns:** a right-aligned colored bullet point on the app card.

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | rest              |
| resource        | Yes      | Url of rest api resource.                                       | url               |
| method          | No       | Method for the api call, default is GET                         | GET,HEAD,OPTIONS,TRACE|
| authentication  | No       | Authentication for the api call, default is None                | None,basic,digest |
| username        | No       | Username to use for auth.                                       | string            |
| password        | No       | Password to use for auth.                                       | string            |
| headers         | No       | Request headers                                                 | json              |
| return_codes    | No       | Acceptable http status codes, x is handled as wildcard          | string            |

> **Working example:**
>```ini
>[http_status_test]
>platform = http_status
>resource = https://google.com
>return_codes = 2xx,3xx
>
>[Google]
>prefix = https://
>url = google.com
>icon = static/images/apps/default.png
>open_in = this_tab
>data_sources = http_status_test
>```

"""

from requests import Request, Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


class Platform:
    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        # set defaults for omitted options
        if not hasattr(self, "method"):
            self.method = "GET"
        if not hasattr(self, "authentication"):
            self.authentication = None
        if not hasattr(self, "headers"):
            self.headers = None
        if not hasattr(self, "return_codes"):
            self.return_codes = "2xx,3xx"

    def process(self):
        # Check if method is within allowed methods for http_status
        if self.method.upper() not in ["GET", "HEAD", "OPTIONS", "TRACE"]:
            raise NotImplementedError

        s = Session()
        # prepare Authentication mechanism
        if self.authentication:
            if self.authentication.lower() == "digest":
                auth = HTTPDigestAuth(self.username, self.password)
            else:
                auth = HTTPBasicAuth(self.username, self.password)
        else:
            auth = None

        # Send request
        req = Request(self.method.upper(), self.resource, headers=self.headers, auth=auth)
        prepped = req.prepare()
        resp = s.send(prepped)

        return_codes = tuple([x.replace('x', '') for x in self.return_codes.split(',')])

        if str(resp.status_code).startswith(return_codes):
            icon_class = "theme-success-text"
        else:
            icon_class = "theme-failure-text"

        return f"<i class='material-icons right {icon_class}'>fiber_manual_record </i>"
