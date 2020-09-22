# DashMachine
### Another web application bookmark dashboard, with fun features.
![Subreddit subscribers](https://img.shields.io/reddit/subreddit-subscribers/dashmachine?style=social)

![GitHub last commit](https://img.shields.io/github/last-commit/rmountjoy92/dashmachine)
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/rmountjoy/dashmachine)

![Docker Pulls](https://img.shields.io/docker/pulls/rmountjoy/dashmachine)
![GitHub Repo stars](https://img.shields.io/github/stars/rmountjoy92/dashmachine?style=social)

![GitHub repo size](https://img.shields.io/github/repo-size/rmountjoy92/dashmachine)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/rmountjoy/dashmachine/latest?label=Docker%20Image%20Size)
![Lines of code](https://img.shields.io/tokei/lines/github/rmountjoy92/dashmachine)

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

[![Donate](https://img.shields.io/badge/$-support-ff69b4.svg?style=flat)](https://liberapay.com/rmountjoy) 
![Bountysource](https://img.shields.io/bountysource/team/dashmachine/activity)

Want a feature added now? [Open a bounty](https://www.bountysource.com/teams/dashmachine-app)

## Screenshots

![screenshot](https://raw.githubusercontent.com/rmountjoy92/DashMachine/master/screenshot1.png)

![screenshot](https://raw.githubusercontent.com/rmountjoy92/DashMachine/master/screenshot2.png)

![screenshot](https://raw.githubusercontent.com/rmountjoy92/DashMachine/master/screenshot3.png)

![screenshot](https://raw.githubusercontent.com/rmountjoy92/DashMachine/master/screenshot4.png)


## Installation
### Docker
```
docker create \
  --name=dashmachine \
  -p 5000:5000 \
  -v path/to/data:/dashmachine/dashmachine/user_data \
  --restart unless-stopped \
  rmountjoy/dashmachine:latest
```
To run in a subfolder, use a CONTEXT_PATH environment variable. For example, to run at localhost:5000/dash:
```
docker create \
  --name=dashmachine \
  -p 5000:5000 \
  -e CONTEXT_PATH=/dash
  -v path/to/data:/dashmachine/dashmachine/user_data \
  --restart unless-stopped \
  rmountjoy/dashmachine:latest
```
### Synology
Check out this awesome guide: https://nashosted.com/manage-your-self-hosted-applications-using-dashmachine/
### Python
Instructions are for linux.
```
virtualenv --python=python3 DashMachineEnv
cd DashMachineEnv && source bin/activate
git clone https://github.com/rmountjoy92/DashMachine.git
cd DashMachine && pip install -r requirements.txt
python3 run.py
```
Then open a web browser and go to localhost:5000

## Default user/password
```
User: admin
Password: admin
```

## Updating
For python, use git. For docker, just pull the latest image and recreate the container.

## Configuration
The user data folder is located at DashMachine/dashmachine/user_data. This is where the config.ini, custom backgrounds/icons, and the database file live. A reference for what can go into the config.ini file can be found on the settings page of the dashmachine by clicking the info icon next to 'Config'. 

### Note
If you change the config.ini file, you either have to restart the container (or python script) or click the 'save' button in the config section of settings for the config to be applied. Pictures added to the backgrounds/icons folders are available immediately.

## Want to contribute?
Please use the pull request template at:
https://github.com/rmountjoy92/DashMachine/blob/master/pull_request_template.md

See this link for how to create a pull request:
https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request

## Tech used
* Flask (Python 3)
* SQLalchemy w/ SQLite database
* HTML5/Jinja2
* Materialize css
* JavaScript/jQuery/jQueryUI
* .ini (for configuration)

## FAQs
1. application does not work in iframe
see https://github.com/rmountjoy92/DashMachine/issues/6
