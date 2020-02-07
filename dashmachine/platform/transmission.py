import json
from flask import render_template_string
import transmissionrpc


# from pprint import PrettyPrinter
# pp = PrettyPrinter()


class Platform:
    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "port"):
            self.port = 9091
        if not hasattr(self, "host"):
            self.host = "localhost"

        self.tc = transmissionrpc.Client(
            self.host, port=self.port, user=self.user, password=self.password
        )

    def process(self):

        torrents = len(self.tc.get_torrents())
        data = {}
        for key, field in self.tc.session_stats().__dict__["_fields"].items():
            data[key] = field.value
        # pp.pprint (data)

        value_template = render_template_string(self.value_template, **data)
        return value_template


# Testing
# test = Platform(host='192.168.1.19', user='', password='').process()
