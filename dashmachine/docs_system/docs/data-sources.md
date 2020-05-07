### Data Sources
Data sources provide information to cards on the dashboard. Here's how it works in a nutshell:

1. If a card is configured with a data source, once the dashboard has loaded, the web client will go through each data source and request information from the server.
2. A data source 'platform' on the server handles the information request, and returns html to the web client.
3. The web client then appends the returned html in the 'data source container' on the card.

<div class="divider"></div>

##### For apps the 'data source container' is this area:

![ds-container](/static/images/docs/app-ds-container.png)


##### For custom cards the 'data source container' is this area:

![ds-container](/static/images/docs/custom-ds-container.png)

<div class="divider"></div>

##### What are 'platforms' and what can they do?
Platforms are simply a python file on the server, set up to take in configuration data from the config.ini and return html back to the web interface. The platforms included with DM are found at `DashMachine/dashmachine/platform`. This is the 'official' set of data source platforms created for DM by Ross and the community.
<br>
Some examples on what a platform can do:

- Any data creation/manipulation that the Python language is capable of
- make calls on REST APIs
- format data as html
- return html with javascript to create interactive cards, or interact with the DOM
- register new API resources on the DM server.

<div class="divider"></div>

##### Value Templates
Some platforms allow for the user to create the template for the data source in the configuration. The platform will provide a number of variables the user's template will have access to. If you see a platform with a variable `value_template`, you will need to set it as a jinja template html string. For example, the `pihole` platform provides `"domain_count", "queries", "blocked", "ads_percentage", "unique_domains", "forwarded", "cached", "total_clients", "unique_clients", "total_queries", "gravity_last_updated"`. So our value template could look like:
```ini
value_template = Ads Blocked Today: {{ blocked }}<br>Status: {{ status }}<br>Queries today: {{ queries }}
```
See [Jinja Templating](https://jinja.palletsprojects.com/en/2.11.x/templates/)