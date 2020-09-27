#### Main Settings

##### Settings
This is the configuration entry for DashMachine's settings. DashMachine will not work if this is missing. As for all config entries, [Settings] can only appear once in the config. If you change the config.ini file, you either have to restart the container (or python script) or click the ‘save’ button in the config section of settings for the config to be applied.
```ini
[Settings]
theme = light
accent = orange
background = None
roles = admin,user,public_user
home_access_groups = admin_only
settings_access_groups = admin_only
custom_app_title = DashMachine
sidebar_default = open
tags_expanded = True
```

| Variable               | Required | Description                                              | Options                                                                                                                                                                        |
|------------------------|----------|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Settings]             | Yes      | Config section name.                                                          | [Settings]                                                                                                                                                                     |
| theme                  | Yes      | UI theme.                                                                     | light, dark                                                                                                                                                                    |
| accent                 | Yes      | UI accent color                                                               | orange, red, pink, purple, deepPurple, indigo, blue, lightBlue,cyan, teal, green, lightGreen, lime, yellow, amber, deepOrange, brown, grey, blueGrey                           |
| cardcolor              | Yes      | Card Color. Defines if the card should use the UI-Accent color                | True or False (Default: False)                                                                                                                                                 |
| background             | Yes      | Background image for the UI                                                   | /static/images/backgrounds/yourpicture.png, external link to image, None, random                                                                                               |
| roles                  | No       | User roles for access groups.                                                 | comma separated string, if not defined, this is set to 'admin,user,public_user'. Note: admin, user, public_user roles are required and will be added automatically if omitted. |
| home_access_groups     | No       | Define which access groups can access the /home page                          | Groups defined in your config. If not defined, default is admin_only                                                                                                           |
| settings_access_groups | No       | Define which access groups can access the /settings page                      | Groups defined in your config. If not defined, default is admin_only                                                                                                           |
| custom_app_title       | No       | Change the title of the app for browser tabs                                  | string                                                                                                                                                                         |
| sidebar_default        | No       | Select the default state for the sidebar                                      | open, closed, no_sidebar                                                                                                                                                       |
| tags                   | No       | Set custom options for your tags. Json options are "name", "icon", "sort_pos" | comma separated json dicts. For "icon" use material design icons: https://material.io/resources/icons                                                                          |
| tags_expanded          | No       | Set to False to have your tags collapsed by default                           | True, False                                                                                                                                                   |

##### Users
Each user requires a config entry, and there must be at least one user in the config (otherwise the default user is added). Each user has a username, a role for configuring access groups, and a password. By default there is one user, named 'admin', with role 'admin' and password 'admin'. To change this user's name, password or role, just modify the config entry's variables and press save. To add a new user, add another user config entry UNDER all existing user config entries. A user with role 'admin' must appear first in the config. Do not change the order of users in the config once they have been defined, otherwise their passwords will not match the next time the config is applied. When users are removed from the config, they are deleted and their cached password is also deleted when the config is applied.
```ini
[admin]
role = admin
password = admin
confirm_password = admin
```

| Variable         | Required | Description                                                                                                                                                                                                                            | Options          |
|------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| [Username]       | Yes      | The user's name for logging in                                                                                                                                                                                                         | [Username]       |
| role             | Yes      | The user's role. This is used for access groups and controlling who can view /home and /settings. There must be at least one 'admin' user, and it must be defined first in the config. Otherwise, the first user will be set to admin. | string           |
| password         | No       | Add a password to this variable to change the password for this user. The password will be hashed, cached and removed from the config. When adding a new user, specify the password, otherwise 'admin' will be used.                   | string           |
| confirm_password | No       | When adding a new user or changing an existing user's password you must confirm the password in this variable                                                                                                                          | string           |
| theme            | No       | Override the theme from Settings for this user                                                                                                                                                                                         | same as Settings |
| accent           | No       | Override the accent from Settings for this user                                                                                                                                                                                        | same as Settings |
| sidebar_default  | No       | Override the sidebar_default from Settings for this user                                                                                                                                                                               | same as Settings |

##### Access Groups
You can create access groups to control what user roles can access parts of the ui. Access groups are just a collection of roles, and each user has an attribute 'role'. Each application can have an access group, if the user's role is not in the group, the app will be hidden. Also, in the settings entry you can specify `home_access_groups` and `settings_access_groups` to control which groups can access /home and /settings
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
