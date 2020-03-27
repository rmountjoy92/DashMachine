
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
| description  | No       | A short description for the app.                                                                                                    | string                                                       |
| data_sources | No       | Data sources to be included on the app's card.*Note: you must have a data source set up in the config above this application entry. | comma separated string                                       |
| tags         | No       | Optionally specify tags for organization on /home                                                                                   | comma separated string                                       |
| groups       | No       | Optionally specify the access groups that can see this app.                                                                         | comma separated string                                       |

##### Collection
These entries provide a card on the dashboard containing a list of links.
```ini
[Collection Name]
type = collection
icon = collections_bookmark
urls = {"url": "google.com", "icon": "static/images/apps/default.png", "name": "Google", "open_in": "new_tab"},{"url": "duckduckgo.com", "icon": "static/images/apps/default.png", "name": "DuckDuckGo", "open_in": "iframe"}
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
| tags              | No       | Optionally specify tags for organization on /home                                            | comma separated string              |
| groups            | No       | Optionally specify the access groups that can see this app.                                  | comma separated string              |