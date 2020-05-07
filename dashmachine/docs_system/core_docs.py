import os
import importlib
from dashmachine.paths import platform_folder
from dashmachine.main.models import DataSources

doc_toc_string = """
<a name="top"></a>
### Platforms
{% for doc_dict in doc_dicts %}
> - [{{ doc_dict['name'] }}](#{{ doc_dict['name'] }})
{% endfor %}
"""

base_md_string = """
{% if doc_dict['author'] %}
[↑ Go to top](#top)
<br>
{% endif %}
### {{ doc_dict['name'] }}
{{ doc_dict['description'] }}

{%+ if doc_dict['author'] -%}
- Author: [{{ doc_dict['author'] }}]({{ doc_dict['author_url'] }})
{% endif %}
{%+ if doc_dict['version'] -%}
- Version: {{ doc_dict['version'] }}
{% endif %}
{%+ if doc_dict['returns'] -%}
- Returns: {{ doc_dict['returns'] }}
{% endif %}
{%+ if doc_dict['returns_json_keys'] -%}
- Available template variables: {% for key in doc_dict['returns_json_keys'] %}"{{key}}", {% endfor %}
{% endif %}

##### Default config
```ini
{{ doc_dict['variables'][0]['variable'] }}
{%+ for variable in doc_dict['variables'][1:] -%}
{{ variable['variable'] }} = {{ variable['default']|safe }}
{%+ endfor -%}
```

| Variable                   | Description                   | Default                   | Options                   |
|----------------------------|-------------------------------|---------------------------|---------------------------|
{%+ for variable in doc_dict['variables'] -%}
| {{ variable['variable'] }} | {{ variable['description'] }} | {{ variable['default']|replace("|","&#124;")|safe }} | {{ variable['options'] }} |
{% endfor %}

{%+ for variable in doc_dict['variables'] -%}
{% if variable['variables']|length > 0 %}
<br>
>##### {{ variable['variable'] }}
>```ini
>{{ variable['variable'] }} = { {%- for subvariable in variable['variables'] -%} "{{ subvariable['variable'] }}": "{{ subvariable['default'] }}",{%- endfor -%} }
>```
>| Variable                      | Description                      | Default                      | Options                      |
>|-------------------------------|----------------------------------|------------------------------|------------------------------|
{%+ for subvariable in variable['variables'] -%}
>| {{ subvariable['variable'] }} | {{ subvariable['description'] }} | {{ subvariable['default']|safe }} | {{ subvariable['options'] }} |
{% endfor %}
{% endif %}
{% endfor %}

{% if doc_dict['example']|length > 0 %}
##### Example
{{ doc_dict['example']|safe }}
{% endif %}

<div class="divider"></div>
"""
settings_doc_dict = {
    "name": "Settings",
    "description": "This is the configuration entry for DashMachine's settings. DashMachine will not work if this is missing. As for all config entries, [Settings] can only appear once in the config. If you change the config.ini file, you either have to restart the container (or python script) or click the ‘save’ button in the config section of settings for the config to be applied.",
    "variables": [
        {
            "variable": "[Settings]",
            "description": "Config section name.",
            "default": "",
            "options": ".ini header",
        },
        {
            "variable": "theme",
            "description": "UI theme",
            "default": "light",
            "options": "light, dark",
        },
        {
            "variable": "accent",
            "description": "UI accent color",
            "default": "orange",
            "options": "orange, red, pink, purple, deepPurple, indigo, blue, lightBlue,cyan, teal, green, lightGreen, lime, yellow, amber, deepOrange, brown, grey, blueGrey",
        },
        {
            "variable": "background",
            "description": "Background image for the UI",
            "default": "None",
            "options": "/static/images/backgrounds/yourpicture.png, external link to image, None, random",
        },
        {
            "variable": "roles",
            "description": "User roles for access groups.",
            "default": "admin,user,public_user",
            "options": "comma separated string, Note: admin, user, public_user roles are required and will be added automatically if omitted.",
        },
        {
            "variable": "custom_app_title",
            "description": "Change the title of the app for browser tabs",
            "default": "Dashmachine",
            "options": "string",
        },
        {
            "variable": "tags_expanded",
            "description": "Set to False to have your tags collapsed by default",
            "default": "True",
            "options": "True, False",
        },
        {
            "variable": "tags",
            "description": "Set custom options for your tags",
            "default": '{"name": "","icon": "","sort_pos": "",}',
            "options": "comma separated json dicts",
            "variables": [
                {
                    "variable": "name",
                    "description": "The name of the tag",
                    "default": "",
                    "options": "string",
                },
                {
                    "variable": "icon",
                    "description": "The icon for the tag",
                    "default": "",
                    "options": "Use material design icons: https://material.io/resources/icons",
                },
                {
                    "variable": "sort_pos",
                    "description": "The sort position for the tag",
                    "default": "",
                    "options": "number",
                },
            ],
        },
        {
            "variable": "action_providers",
            "description": "Set custom actions for the search bars. In the search bar, press '!' followed by your configured macro to run the action. A common action would be running a search on a search provider.",
            "default": '{"name": "Google","macro": "g","action": "https://www.google.com/search?q={{ value }}"}',
            "options": "comma separated json dicts",
            "variables": [
                {
                    "variable": "name",
                    "description": "The name of the action",
                    "default": "Google",
                    "options": "string",
                },
                {
                    "variable": "macro",
                    "description": "A key or set of keys that you will type after '!'",
                    "default": "g",
                    "options": "string",
                },
                {
                    "variable": "action",
                    "description": "jinja template url with the value of the search bar available as 'value'.",
                    "default": "https://www.google.com/search?q={{ value }}",
                    "options": "jinja template",
                },
            ],
        },
    ],
}

access_groups_doc_dict = {
    "name": "Access Groups",
    "description": "You can create access groups to control what user roles can access parts of the ui. Access groups are just a collection of roles, and each user has an attribute 'role'. Each application can have an access group, if the user's role is not in the group, the app will be hidden.",
    "variables": [
        {
            "variable": "[name]",
            "description": "Name for access group.",
            "default": "",
            "options": ".ini header",
        },
        {
            "variable": "roles",
            "description": "A comma separated list of user roles allowed to view apps in this access group",
            "default": "admin",
            "options": "Roles defined in your config.",
        },
        {
            "variable": "can_access_home",
            "description": "Control if this user is allowed to access /home",
            "default": "True",
            "options": "True,False",
        },
        {
            "variable": "can_access_user_settings",
            "description": "Control if this user is allowed to access their user settings",
            "default": "True",
            "options": "True,False",
        },
        {
            "variable": "can_access_main_settings",
            "description": "Control if this user is allowed to access the global dashmachine settings.",
            "default": "False",
            "options": "True,False",
        },
        {
            "variable": "can_access_card_editor",
            "description": "Control if this user is allowed to access the card editor",
            "default": "False",
            "options": "True,False",
        },
        {
            "variable": "can_access_raw_config",
            "description": "Control if this user is allowed to access the config.ini editor",
            "default": "False",
            "options": "True,False",
        },
        {
            "variable": "can_access_docs",
            "description": "Control if this user is allowed to access the documentation",
            "default": "False",
            "options": "True,False",
        },
        {
            "variable": "can_see_sidenav",
            "description": "Control if this user is allowed to see the sidenav",
            "default": "True",
            "options": "True,False",
        },
        {
            "variable": "can_edit_users",
            "description": "Control if this user is allowed edit other users and their settings",
            "default": "False",
            "options": "True,False",
        },
        {
            "variable": "can_edit_images",
            "description": "Control if this user is allowed edit images in settings",
            "default": "False",
            "options": "True,False",
        },
    ],
}

user_settings_doc_dict = {
    "name": "Users",
    "description": "Each user requires a config entry, and there must be at least one user in the config (otherwise the default user is added). Each user has a username, a role for configuring access groups, and a password. By default there is one user, named 'admin', with role 'admin' and password 'admin'. To change this user's name, password or role, just modify the config entry's variables and press save. To add a new user, add another user config entry UNDER all existing user config entries. A user with role 'admin' must appear first in the config. Do not change the order of users in the config once they have been defined, otherwise their passwords will not match the next time the config is applied. When users are removed from the config, they are deleted and their cached password is also deleted when the config is applied.",
    "variables": [
        {
            "variable": "[username]",
            "description": "The user's name for logging in.",
            "default": "admin",
            "options": ".ini header",
        },
        {
            "variable": "role",
            "description": "The user's role. This is used for access groups and controlling who can view /home and /settings. There must be at least one 'admin' user, and it must be defined first in the config. Otherwise, the first user will be set to admin.",
            "default": "admin",
            "options": "string",
        },
        {
            "variable": "password",
            "description": "Add a password to this variable to change the password for this user. The password will be hashed, cached and removed from the config. When adding a new user, specify the password, otherwise 'admin' will be used.",
            "default": "",
            "options": "string",
        },
        {
            "variable": "confirm_password",
            "description": "When adding a new user or changing an existing user's password you must confirm the password in this variable",
            "default": "",
            "options": "string",
        },
        {
            "variable": "theme",
            "description": "Override the theme from Settings for this user",
            "default": "",
            "options": "same as Settings",
        },
        {
            "variable": "accent",
            "description": "Override the accent from Settings for this user",
            "default": "",
            "options": "same as Settings",
        },
        {
            "variable": "background",
            "description": "Override the background from Settings for this user",
            "default": "",
            "options": "same as Settings",
        },
        {
            "variable": "tags_expanded",
            "description": "Override the tags_expanded from Settings for this user",
            "default": "",
            "options": "same as Settings",
        },
    ],
}

apps_doc_dict = {
    "name": "App",
    "description": "These entries are the standard card type for displaying apps on your dashboard and sidenav.",
    "variables": [
        {
            "variable": "[name]",
            "description": "The name of your app. ",
            "default": "",
            "options": ".ini header",
        },
        {
            "variable": "prefix",
            "description": "The prefix for the app's url. ",
            "default": "https://",
            "options": "web prefix, e.g. http:// or https://",
        },
        {
            "variable": "url",
            "description": "The url for your app.",
            "default": "",
            "options": "web url, e.g. myapp.com",
        },
        {
            "variable": "open_in",
            "description": "open the app in the current tab, an iframe or a new tab",
            "default": "this_tab",
            "options": "web url, e.g. myapp.com ",
        },
        {
            "variable": "icon",
            "description": "Icon for the dashboard.",
            "default": "static/images/apps/default.png",
            "options": "/static/images/icons/yourpicture.png, external link to image",
        },
        {
            "variable": "sidebar_icon",
            "description": "Icon for the sidenav.",
            "default": "static/images/apps/default.png",
            "options": "/static/images/icons/yourpicture.png, external link to image",
        },
        {
            "variable": "description",
            "description": "A short description for the app.",
            "default": "",
            "options": "HTML",
        },
        {
            "variable": "data_sources",
            "description": "Data sources to be included on the app's card.*Note: you must have a data source set up in the config above this application entry.",
            "default": "",
            "options": "comma separated string",
        },
        {
            "variable": "tags",
            "description": "Optionally specify tags for organization on /home",
            "default": "",
            "options": "comma separated string",
        },
        {
            "variable": "groups",
            "description": "Optionally specify the access groups that can see this app.",
            "default": "",
            "options": "comma separated string",
        },
    ],
}

collections_doc_dict = {
    "name": "Collection",
    "description": "These entries provide a card on the dashboard containing a list of links.",
    "variables": [
        {
            "variable": "[name]",
            "description": "Name for the collection",
            "default": "",
            "options": ".ini header",
        },
        {
            "variable": "type",
            "description": "This tells DashMachine what type of card this is.",
            "default": "collection",
            "options": "collection",
            "disabled": "True",
        },
        {
            "variable": "icon",
            "description": "The material design icon class for the collection.",
            "default": "collections_bookmark",
            "options": "https://material.io/resources/icons",
        },
        {
            "variable": "tags",
            "description": "Optionally specify tags for organization on /home",
            "default": "",
            "options": "comma separated string",
        },
        {
            "variable": "groups",
            "description": "Optionally specify the access groups that can see this app.",
            "default": "",
            "options": "comma separated string",
        },
        {
            "variable": "urls",
            "description": "The urls to include in your collection.",
            "default": '{"url": "https://google.com", "icon": "static/images/apps/default.png", "name": "Google", "open_in": "new_tab"},{"url": "https://duckduckgo.com", "icon": "static/images/apps/default.png", "name": "DuckDuckGo", "open_in": "this_tab"}',
            "options": "comma separated json dicts",
            "variables": [
                {
                    "variable": "url",
                    "description": "The url for the collection item",
                    "default": "https://google.com",
                    "options": "web url",
                },
                {
                    "variable": "icon",
                    "description": "The icon for the collection item",
                    "default": "static/images/apps/default.png",
                    "options": "/static/images/icons/yourpicture.png, external link to image",
                },
                {
                    "variable": "open_in",
                    "description": "Which mode to open the link in",
                    "default": "this_tab",
                    "options": "this_tab,new_tab",
                },
            ],
        },
    ],
}
custom_card_example = """
```ini
[variable_name]
platform = weather
woeid = 2514815

[custom_card_name]
type = custom
data_sources = variable_name
```
"""
custom_card_doc_dict = {
    "name": "Custom Card",
    "description": "These entries provide an empty card on the dashboard to be populated by a data source. This allows the data source to populate the entire card.",
    "example": custom_card_example,
    "variables": [
        {
            "variable": "[name]",
            "description": "Name for the custom card",
            "default": "",
            "options": ".ini header",
        },
        {
            "variable": "type",
            "description": "This tells DashMachine what type of card this is.",
            "default": "custom",
            "options": "custom",
            "disabled": "True",
        },
        {
            "variable": "data_sources",
            "description": "What data sources to display on the card.",
            "default": "",
            "options": "comma separated string",
        },
        {
            "variable": "tags",
            "description": "Optionally specify tags for organization on /home",
            "default": "",
            "options": "comma separated string",
        },
        {
            "variable": "groups",
            "description": "Optionally specify the access groups that can see this app.",
            "default": "",
            "options": "comma separated string",
        },
    ],
}


def data_sources_doc_dicts(platform_name=None, get_all=False):
    if platform_name:
        platform_names = [platform_name]
    elif get_all:
        platform_names = [
            file.replace(".py", "") for file in os.listdir(platform_folder)
        ]
        platform_names.remove("__pycache__")
        platform_names.remove("__init__")

    data_source_dicts = []
    for name in platform_names:
        module = importlib.import_module(f"dashmachine.platform.{name}", ".")
        platform = module.Platform()
        if getattr(platform, "docs", None):
            docs = platform.docs()
            data_source_dicts.append(docs)
    return data_source_dicts


def configured_data_sources_doc_dicts(data_source_id=None, get_all=False):
    if data_source_id:
        data_sources = [DataSources.query.filter_by(id=data_source_id).first()]
    elif get_all:
        data_sources = DataSources.query.all()

    data_source_dicts = []
    for data_source in data_sources:
        data_source_dict = {
            "id": data_source.id,
            "name": data_source.name,
            "platform": data_source.platform,
        }
        module = importlib.import_module(
            f"dashmachine.platform.{data_source.platform}", "."
        )
        platform = module.Platform()
        docs = platform.docs()
        for key, value in docs.items():
            data_source_dict[key] = value
        data_source_dicts.append(data_source_dict)
    if data_source_id:
        return data_source_dicts[0]
    return data_source_dicts
