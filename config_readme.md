#### Config.ini Readme

##### Settings
This is the configuration entry for DashMachine's settings. DashMachine will not work if
this is missing. As for all config entries, [Settings] can only appear once in the config.
If you change the config.ini file, you either have to restart the container 
(or python script) or click the ‘save’ button in the config section of settings for the 
config to be applied.
```ini
[Settings]
theme = light
accent = orange
background = None
roles = admin,user,public_user
home_access_groups = admin_only
settings_access_groups = admin_only
custom_app_title = DashMachine
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
| custom_app_title       | No       | Change the title of the app for browser tabs             | string                                                                                                                                                                         |

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
tags = Example Tag
groups = admin_only
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
| tags         | No       | Optionally specify tags for organization on /home                                                                                   | comma separated string                                       |
| groups       | No       | Optionally the access groups that can see this app.                                                                                 | comma separated string                                       |

##### Access Groups
You can create access groups to control what user roles can access parts of the ui. Access groups are just a collection of roles, and each user has an attribute 'role'. Each
application can have an access group, if the user's role is not in the group, the app will be hidden.
Also, in the settings entry you can specify `home_access_groups` and `settings_access_groups` to control
which groups can access /home and /settings
```ini
[admin_only]
roles = admin
```

| Variable     | Required | Description                                                                    | Options                                                                          |
|--------------|----------|--------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| [Group Name] | Yes      | Name for access group.                                                         | [Group Name]                                                                     |
| roles        | Yes      | A comma separated list of user roles allowed to view apps in this access group | Roles defined in your config. If not defined, defaults are admin and public_user |

> Say we wanted to create a limited user that still has a login, but can only access `/home` and certain apps we would first create a group:
>```ini
>[users]
>roles = admin, user
>```
>then we would change in the `[Settings]` entry:
>```ini
>home_access_groups = users
>```
>By default here, the `user` user could access `/home`, but would see no apps. To allow access, we would add to apps:
>```ini
>groups = users
>```
>Say we then wanted to allow some access for users without a login (`public_user`), we would add:
>```ini
>[public]
>roles = admin, user, public_user
>```
>then we would change in the `[Settings]` entry:
>```ini
>home_access_groups = public
>```
>By default here, the `public_user` user could access `/home`, but would see no apps. To allow access, we would add to apps:
>```ini
>groups = public
>```


>It’s also important to note, when setting up roles in `[Settings]`, say we had roles set like this:
>```ini
>roles = my_people
>```
>Dashmachine will automatically add `admin,user,public_user`, so really you would have 4 roles: `my_people,admin,user,public_user`. Also, the `admin_only` group is required and added by default if omitted.

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