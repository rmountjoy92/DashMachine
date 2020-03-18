"""

##### ping
Check if a service is online.
```ini
[variable_name]
platform = ping
resource = 192.168.1.1
```
> **Returns:** a right-aligned colored bullet point on the app card.

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | rest              |
| resource        | Yes      | Url of whatever you want to ping                                | url               |


"""

import platform
import subprocess


class Platform:
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
