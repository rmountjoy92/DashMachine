from requests import Request, Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


class Platform:
    def docs(self):
        documentation = {
            "name": "http_status",
            "author": "franznemeth",
            "author_url": "https://github.com/franznemeth",
            "version": 1.0,
            "description": "Make a http call on a given URL and display if the service is online.",
            "example": """
```ini
[http_status_test]
platform = http_status
resource = https://google.com
return_codes = 2xx,3xx

[Google]
prefix = https://
url = google.com
icon = static/images/apps/default.png
open_in = this_tab
data_sources = http_status_test
```
            """,
            "returns": "a right-aligned colored bullet point on the app card.",
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
                    "default": "http_status",
                    "options": "http_status",
                },
                {
                    "variable": "resource",
                    "description": "Url of rest api resource.",
                    "default": "https://google.com",
                    "options": "url",
                },
                {
                    "variable": "method",
                    "description": "Method for the api call",
                    "default": "GET",
                    "options": "GET,HEAD,OPTIONS,TRACE",
                },
                {
                    "variable": "authentication",
                    "description": "Authentication for the api call",
                    "default": "",
                    "options": "None,basic,digest",
                },
                {
                    "variable": "username",
                    "description": "Username to use for auth.",
                    "default": "",
                    "options": "string",
                },
                {
                    "variable": "password",
                    "description": "Password to use for auth.",
                    "default": "",
                    "options": "string",
                },
                {
                    "variable": "headers",
                    "description": "Request headers",
                    "default": "",
                    "options": "json",
                },
                {
                    "variable": "return_codes",
                    "description": "Acceptable http status codes, x is handled as wildcard",
                    "default": "2xx,3xx",
                    "options": "string",
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
        if not hasattr(self, "authentication"):
            self.authentication = None
        if not hasattr(self, "headers"):
            self.headers = None
        if not hasattr(self, "return_codes"):
            self.return_codes = "2xx,3xx"
        if not hasattr(self, "ssl_ignore"):
            self.ssl_ignore = "No"

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
        req = Request(
            self.method.upper(), self.resource, headers=self.headers, auth=auth
        )
        prepped = req.prepare()
        if self.ssl_ignore == "yes":
            resp = s.send(prepped, verify=False)
        else:
            resp = s.send(prepped)
        resp = s.send(prepped)

        return_codes = tuple([x.replace("x", "") for x in self.return_codes.split(",")])

        if str(resp.status_code).startswith(return_codes):
            icon_class = "theme-success-text"
        else:
            icon_class = "theme-failure-text"

        return f"<i class='material-icons right {icon_class}'>fiber_manual_record </i>"
