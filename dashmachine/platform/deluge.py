from flask import render_template_string
import requests


class Platform:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "resource"):
            self.resource = "http://localhost/json"

        if not hasattr(self, "password"):
            self.password = ""

        self.id = 1
        self.session = requests.Session()
        self._api_call("auth.login", [self.password])
        self.password = None # Discard password, no longer needed.

    def _api_call(self, method, params=[]):
        json = {
            "id": self.id,
            "method": method,
            "params": params
        }
        return self.session.post(self.resource, json=json)

    def process(self):
        r = self._api_call("web.update_ui", ["download_rate", "upload_rate"])
        json = r.json()
        data = {}
        for key, field in json["result"]["stats"].items():
            data[key] = field

        value_template = render_template_string(self.value_template, **data)
        return value_template
