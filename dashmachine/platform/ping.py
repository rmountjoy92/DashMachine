import platform
import subprocess


class Platform:
    def docs(self):
        documentation = {
            "name": "ping",
            "author": "Nixellion",
            "author_url": "https://github.com/Nixellion",
            "version": 1.0,
            "description": "Check if a service is online.",
            "example": """
```ini
[ping_test]
platform = ping
resource = localhost

[localhost]
prefix = http://
url = localhost
icon = static/images/apps/default.png
open_in = this_tab
data_sources = ping_test
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
                    "default": "ping",
                    "options": "ping",
                },
                {
                    "variable": "resource",
                    "description": "Url of rest api resource.",
                    "default": "localhost",
                    "options": "url",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def process(self):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", self.resource]
        up = subprocess.call(command) == 0

        if up is True:
            icon_class = "theme-success-text"
        else:
            icon_class = "theme-failure-text"

        return f"<i class='material-icons right {icon_class}'>fiber_manual_record </i>"
