from requests import get
from flask import render_template_string


class Platform:
    def __init__(self, data_source, data_source_args):
        self.data_source = data_source
        self.name = data_source["name"]

        # parse the user's options from the config entries
        for source_arg in data_source_args:
            if source_arg.get("key") == "resource":
                self.resource = source_arg.get("value")

            if source_arg.get("key") == "method":
                self.method = source_arg.get("value")

            if source_arg.get("key") == "payload":
                self.payload = source_arg.get("value")

            if source_arg.get("key") == "authentication":
                self.authentication = source_arg.get("value")

            if source_arg.get("key") == "username":
                self.username = source_arg.get("value")

            if source_arg.get("key") == "password":
                self.password = source_arg.get("value")

            if source_arg.get("key") == "value_template":
                self.value_template = source_arg.get("value")

            if source_arg.get("key") == "data_template":
                self.data_template = source_arg.get("value")

            # set defaults for omitted options
            if not hasattr(self, "method"):
                self.method = "GET"

    def process(self):
        if self.method.upper() == "GET":
            try:
                value = get(self.resource).json()
            except Exception as e:
                value = f"{e}"
        value_template = render_template_string(self.value_template, value=value)
        data_template = render_template_string(self.data_template, value=value_template)
        return data_template
