#### Data Source Platforms
DashMachine includes several different 'platforms' for displaying data on your dash applications. Platforms are essentially plugins. All data source config entries require the `platform` variable, which tells DashMachine which platform file in the platform folder to load. **Note:** you are able to load your own platform files by placing them in the platform folder and referencing them in the config. However currently they will be deleted if you update the application, if you would like to make them permanent, submit a pull request for it to be added by default!

> To add a data source to your app, add a data source config entry from one of the samples below
**above** the application entry in config.ini, then add the following to your app config entry:
`data_source = variable_name`