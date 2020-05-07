# Installation
### Default user/password
```
User: admin
Password: admin
```
### Docker
```bash
docker create \
  --name=dashmachine \
  -p 5000:5000 \
  -v path/to/data:/dashmachine/dashmachine/user_data \
  --restart unless-stopped \
  rmountjoy/dashmachine:latest
```
To run in a subfolder, use a CONTEXT_PATH environment variable. For example, to run at localhost:5000/dash:

```bash
docker create \
  --name=dashmachine \
  -p 5000:5000 \
  -e CONTEXT_PATH=/dash
  -v path/to/data:/dashmachine/dashmachine/user_data \
  --restart unless-stopped \
  rmountjoy/dashmachine:latest
```
### Docker Compose

```yaml
version: "2"
services:
   dashmachine:
    image: rmountjoy/dashmachine:latest
    container_name: dashmachine
    restart: unless-stopped
    environment:
        - CONTEXT_PATH: /dash #Optional, only if you want to run dashmachine in a subfolder
    volumes:
        - /path/to/data:/dashmachine/dashmachine/user_data
    ports:
        - 5000:5000 #You can change the port on the left (host) it's already in use, e.g. Synology NAS
```

### Synology
* [Check out this awesome guide](https://nashosted.com/manage-your-self-hosted-applications-using-dashmachine/)

### Python
Instructions are for linux.
```bash
virtualenv --python=python3 DashMachineEnv
cd DashMachineEnv && source bin/activate
git clone https://github.com/rmountjoy92/DashMachine.git
cd DashMachine && pip install -r requirements.txt
python3 run.py
```
Then open a web browser and go to localhost:5000