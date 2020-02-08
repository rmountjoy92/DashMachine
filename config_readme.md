#### Config.ini Readme

##### Settings
This is the configuration entry for DashMachine's settings. DashMachine will not work if
this is missing. As for all config entries, [Settings] can only appear once in the config.
If you change the config.ini file, you either have to restart the container 
(or python script) or click the ‘save’ button in the config section of settings for the 
config to be applied.
```ini
[Settings]
theme = dark
accent = orange
background = static/images/backgrounds/background.png
```

| Variable               | Required | Description                                              | Options                                                                                                                                                                        |
|------------------------|----------|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Settings]             | Yes      | Config section name.                                     | [Settings]                                                                                                                                                                     |
| theme                  | Yes      | UI theme.                                                | light, dark                                                                                                                                                                    |
| accent                 | Yes      | UI accent color                                          | orange, red, pink, purple, deepPurple, indigo, blue, lightBlue,cyan, teal, green, lightGreen, lime, yellow, amber, deepOrange, brown, grey, blueGrey                           |
| background             | Yes      | Background image for the UI                              | /static/images/backgrounds/yourpicture.png, external link to image, None, random                                                                                               |
| roles                  | No       | User roles for access groups.                            | comma separated string, if not defined, this is set to 'admin,user,public_user'. Note: admin, user, public_user roles are required and will be added automatically if omitted. |
| home_access_groups     | No       | Define which access groups can access the /home page     | Groups defined in your config. If not defined, default is admin_only                                                                                                           |
| settings_access_groups | No       | Define which access groups can access the /settings page | Groups defined in your config. If not defined, default is admin_only                                                                                                           |

##### Apps
These entries are the cards that you see one the home page, as well as the sidenav. Entries
must be unique. They are displayed in the order that they appear in config.ini
```ini
[App Name]
prefix = https://
url = your-website.com
icon = static/images/apps/default.png
sidebar_icon = static/images/apps/default.png
description = Example description
open_in = iframe
data_sources = None
```

| Variable     | Required | Description                                                                                                                         | Options                                                      |
|--------------|----------|-------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| [App Name]   | Yes      | The name of your app.                                                                                                               | [App Name]                                                   |
| prefix       | Yes      | The prefix for the app's url.                                                                                                       | web prefix, e.g. http:// or https://                         |
| url          | Yes      | The url for your app.                                                                                                               | web url, e.g. myapp.com                                      |
| open_in      | Yes      | open the app in the current tab, an iframe or a new tab                                                                             | iframe, new_tab, this_tab                                    |
| icon         | No       | Icon for the dashboard.                                                                                                             | /static/images/icons/yourpicture.png, external link to image |
| sidebar_icon | No       | Icon for the sidenav.                                                                                                               | /static/images/icons/yourpicture.png, external link to image |
| description  | No       | A short description for the app.                                                                                                    | string                                                       |
| data_sources | No       | Data sources to be included on the app's card.*Note: you must have a data source set up in the config above this application entry. | comma separated string                                       |

##### Access Groups
You can create access groups to control what user roles can access parts of the ui. Each
application can have an access group, if the user's role is not in the group, the app will be hidden.
Also, in the settings entry you can specify `home_access_groups` and `settings_access_groups` to control
which groups can access /home and /settings
```ini
[public]
roles = admin, user, public_user
```

> **Note:** if no access groups are defined in the config, the application will create a default group called 'admin_only' with 'roles = admin'

| Variable     | Required | Description                                                                    | Options                                                                          |
|--------------|----------|--------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| [Group Name] | Yes      | Name for access group.                                                         | [Group Name]                                                                     |
| roles        | Yes      | A comma separated list of user roles allowed to view apps in this access group | Roles defined in your config. If not defined, defaults are admin and public_user |

#### Data Source Platforms
DashMachine includes several different 'platforms' for displaying data on your dash applications.
Platforms are essentially plugins. All data source config entries require the `plaform` variable,
which tells DashMachine which platform file in the platform folder to load. **Note:** you are able to
load your own plaform files by placing them in the platform folder and referencing them in the config.
However currently they will be deleted if you update the application, if you would like to make them
permanent, submit a pull request for it to be added by default!

> To add a data source to your app, add a data source config entry from one of the samples below
**above** the application entry in config.ini, then add the following to your app config entry:
`data_source = variable_name`

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
| plaform         | Yes      | Name of the platform.                                           | rest              |
| resource        | Yes      | Url of whatever you want to ping                                | url               |

##### rest
Make a call on a REST API and display the results as a jinja formatted string.
```ini
[variable_name]
platform = rest
resource = https://your-website.com/api
value_template = {{value}}
method = post
authentication = basic
username = my_username
password = my_password
payload = {"var1": "hi", "var2": 1}
```
> **Returns:** `value_template` as rendered string

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| plaform         | Yes      | Name of the platform.                                           | rest              |
| resource        | Yes      | Url of rest api resource.                                       | url               |
| value_template  | Yes      | Jinja template for how the returned data from api is displayed. | jinja template    |
| method          | No       | Method for the api call, default is GET                         | GET,POST          |
| authentication  | No       | Authentication for the api call, default is None                | None,basic,digest |
| username        | No       | Username to use for auth.                                       | string            |
| password        | No       | Password to use for auth.                                       | string            |
| payload         | No       | Payload for post request.                                       | json              |

> **Working example:**
>```ini
>[test]
>platform = rest
>resource = https://pokeapi.co/api/v2/pokemon
>value_template = Pokemon: {{value['count']}}
>
>[Pokemon]
>prefix = https://
>url = pokemon.com
>icon = static/images/apps/default.png
>description = Data sources example
>open_in = this_tab
>data_sources = test
>```