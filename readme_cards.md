
##### Apps
These entries are the standard card type for displaying apps on your dashboard and sidenav.
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
| icon         | Yes      | Icon for the dashboard.                                                                                                             | /static/images/icons/yourpicture.png, external link to image |
| sidebar_icon | No       | Icon for the sidenav.                                                                                                               | /static/images/icons/yourpicture.png, external link to image |
| description  | No       | A short description for the app.                                                                                                    | HTML                                                         |
| data_sources | No       | Data sources to be included on the app's card.*Note: you must have a data source set up in the config above this application entry. | comma separated string                                       |
| tags         | No       | Optionally specify tags for organization on /home                                                                                   | comma separated string                                       |
| groups       | No       | Optionally specify the access groups that can see this app.                                                                         | comma separated string                                       |
| size         | No       | Reduces the height of the card                                                                                                      | small                                                        |

##### Collection
These entries provide a card on the dashboard containing a list of links.
```ini
[Collection Name]
type = collection
icon = collections_bookmark
urls = {"url": "https://google.com", "icon": "static/images/apps/default.png", "name": "Google", "open_in": "new_tab"},{"url": "https://duckduckgo.com", "icon": "static/images/apps/default.png", "name": "DuckDuckGo", "open_in": "this_tab"}
```

| Variable          | Required | Description                                                                                  | Options                             |
|-------------------|----------|----------------------------------------------------------------------------------------------|-------------------------------------|
| [Collection Name] | Yes      | Name for the collection                                                                      | [Collection Name]                   |
| type              | Yes      | This tells DashMachine what type of card this is.                                            | collection                          |
| icon              | No       | The material design icon class for the collection.                                           | https://material.io/resources/icons |
| urls              | Yes      | The urls to include in your collection. Json options are "url", "icon", "name" and "open_in" | comma separated json dicts, "open_in" only has options "this_tab", "new_tab"          |
| tags              | No       | Optionally specify tags for organization on /home                                            | comma separated string              |
| groups            | No       | Optionally specify the access groups that can see this app.                                  | comma separated string              |

##### Custom Card
These entries provide an empty card on the dashboard to be populated by a data source. This allows the data source to populate the entire card.
```ini
[Collection Name]
type = custom
data_sources = my_data_source
```

| Variable          | Required | Description                                                                                  | Options                             |
|-------------------|----------|----------------------------------------------------------------------------------------------|-------------------------------------|
| [Collection Name] | Yes      | Name for the collection                                                                      | [Collection Name]                   |
| type              | Yes      | This tells DashMachine what type of card this is.                                            | custom                              |
| data_sources      | Yes      | What data sources to display on the card.                                                    | comma separated string              |
| tags              | No       | Optionally specify tags for organization on /home                                            | comma separated string              |
| groups            | No       | Optionally specify the access groups that can see this app.                                  | comma separated string              |


> **Working example:**
>```ini
>[test]
>platform = curl
>resource = https://api.myip.com
>value_template = <div class="row center-align"><div class="col s12"><h5><i class="material-icons-outlined" style="position:relative; top: 4px;">dns</i> My IP Address</h5><span class="theme-primary-text">{{value.ip}}</span></div></div>
>response_type = json
>
>[MyIp.com]
>type = custom
>data_sources = test
>```