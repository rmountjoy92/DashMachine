from requests import get


class Platform:
    def __init__(self, data_source, data_source_args):
        # parse the user's options from the config entries
        for key, value in data_source_args.items():
            self.__dict__[key] = value

    def process(self):
        try:
            value = get(self.resource)
        except Exception:
            icon_class = "theme-failure-text"

        if 599 >= value.status_code >= 400:
            icon_class = "theme-failure-text"
        if 399 >= value.status_code >= 300:
            icon_class = "theme-warning-text"
        if 299 >= value.status_code >= 100:
            icon_class = "theme-success-text"

        return f"<i class='material-icons right {icon_class}'>fiber_manual_record </i>"
