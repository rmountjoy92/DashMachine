### Creating Platforms
DashMachine platforms are python plugins loaded by Python's `importlib` module. When they are loaded by DM, they are initialized with their `Platform` class. The official platforms for dashmachine are located at `DashMachine/dashmachine/platform` and are a great resource for learning how they work.
> **NOTE:** When you modify or add one of the files in `DashMachine/dashmachine/platform`, changes will be wiped out by updates. If you want to experiment with your own platforms, put them in `DashMachine/dashmachine/user_data/platform` to persist updates.

<div class="divider"></div>

##### A minimal platform
Let's start by making a super simple platform. It's just going to return 'Hello World' to the card's data source container. First add a file called `hello_world.py` in `DashMachine/dashmachine/user_data/platform` with the contents:
```python
class Platform:
    def docs(self):
        # This is the function DM calls to get the metadata about your plaform.
        # This is what DM uses to generate the documentation and options in the gui forms.
        # It is very important that this information is correct.
        documentation = {
            "name": "hello_world",
            "author": "RMountjoy",
            "author_url": "https://github.com/rmountjoy92",
            "version": 1.0,
            "description": "return 'Hello World' to the card's data source container",
            "returns": "Hello World",
            "variables": [
                {
                    "variable": "[variable_name]",
                    "description": "Name for the data source.",
                    "default": "",
                    "options": ".ini header",
                },
                {
                    "variable": "platform",
                    "description": "Name of the platform.",
                    "default": "hello_world",
                    "options": "hello_world",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        # This is the initialization function.
        # This should be reserved for setting up the platform's configuration.
        # NOTE: this is not where you call APIs, as this code is run every time DM
        # initializes your 'Platform' class (e.g. to pull documentation, etc).
        
        # These following two lines parses the options supplied by the user in their config.ini
        for key, value in kwargs.items():
            self.__dict__[key] = value
    
    def process(self):
        # this is the function that is ran when the web client requests
        # information from this platform (e.g. when the dashboard is loaded)
        # this is where you call APIs, or whatever you're doing to get data.
        return "Hello World"
```

**NOTE:** After you add a new platform file to your user_data/platforms folder, you will need to restart DashMachine for the platform to be available.

Then, we would add the following two entries to our config.ini **NOTE** All custom platforms must be prefixed with `custom_` when they are referenced in a `data_source` entry:
```ini
[hello_world_ds]
platform = custom_hello_world

[hello_world]
type = custom
data_sources = hello_world_ds
```
Now, on your dashboard, you should see this:

![ds-container](/static/images/docs/hello-world-ds-example1.png)

Ugly right!? Which leads us to the next section,

<div class="divider"></div>

##### Rendering HTML
Let's make some changes to our `hello_world.py` file, at the top of the file we would add:
```python
from flask import render_template_string
```
then we would change our `process()` method like so:
```python
def process(self):
    text_to_display = "Hello World"
    html_string = """
    <div class="row center-align">
        <div class="col s12">
            <i class="material-icons-outlined theme-primary-text medium">language</i>
            <h5 class="font-weight-900">{{ text_to_display }}</h5>
        </div>
    </div>
    """
    return render_template_string(html_string, text_to_display=text_to_display)
```
Much better:

![ds-container](/static/images/docs/hello-world-ds-example2.png)

For a full reference of the html elements you have available to you, check out:

* [Materialize CSS](https://materializecss.com/)
* [Material Icons](https://material.io/resources/icons/?icon=settings&style=outline)

Remeber that your returned HTML can include `script` and `style` tags for including js/jquery/css

<div class="divider"></div>

##### Utilizing user configuration
Okay, let's say that instead of displaying our fixed 'Hello World' message, we'll display the `text_to_display` variable from their configuration. So the entries in the .ini file would look like:
```ini
[hello_world_ds]
platform = custom_hello_world
text_to_display = Hi there.

[hello_world]
type = custom
data_sources = hello_world_ds
```
and in our `hello_world.py` file the only thing we would have to change is:
```python
return render_template_string(html_string, text_to_display=text_to_display)
```
changes to:
```python
return render_template_string(html_string, text_to_display=self.text_to_display)
```
So, now our card displays whatever `text_to_display` is set to:

![ds-container](/static/images/docs/hello-world-ds-example3.png)


**NOTE:** Now that we have added a configuration option, we need to update our `docs()` method, otherwise our new option will not show up in gui forms:
```python
def docs(self):
    documentation = {
        "name": "hello_world",
        "author": "RMountjoy",
        "author_url": "https://github.com/rmountjoy92",
        "version": 1.0,
        "description": "return the value of 'text_to_display' to the card's data source container",
        "returns": "text_to_display as formatted html",
        "variables": [
            {
                "variable": "[variable_name]",
                "description": "Name for the data source.",
                "default": "",
                "options": ".ini header",
            },
            {
                "variable": "platform",
                "description": "Name of the platform.",
                "default": "hello_world",
                "options": "hello_world",
            },
            {
                "variable": "text_to_display",
                "description": "the text to display on the card",
                "default": "Hello World",
                "options": "string",
            },
        ],
    }
    return documentation
```
You'll notice on the new variable we just made that there is a `default` field. We need to make sure we have defaults set up for our configuration options, so users don't have to fill out optional configurations. To do so, we would rewrite our `__init__()` method like so:
```python
def __init__(self, *args, **kwargs):
    for key, value in kwargs.items():
        self.__dict__[key] = value
    
    if not hasattr(self, "text_to_display"):
        self.text_to_display = "Hello World"
```
To sum it all up, here is our user configurable version of our hello world platform:
```python
from flask import render_template_string


class Platform:
    def docs(self):
        documentation = {
            "name": "hello_world",
            "author": "RMountjoy",
            "author_url": "https://github.com/rmountjoy92",
            "version": 1.0,
            "description": "return the value of 'text_to_display' to the card's data source container",
            "returns": "text_to_display as formatted html",
            "variables": [
                {
                    "variable": "[variable_name]",
                    "description": "Name for the data source.",
                    "default": "",
                    "options": ".ini header",
                },
                {
                    "variable": "platform",
                    "description": "Name of the platform.",
                    "default": "hello_world",
                    "options": "hello_world",
                },
                {
                    "variable": "text_to_display",
                    "description": "the text to display on the card",
                    "default": "Hello World",
                    "options": "string",
                },
            ],
        }
        return documentation

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
    
        if not hasattr(self, "text_to_display"):
            self.text_to_display = "Hello World"
        

    def process(self):
        html_string = """
        <div class="row center-align">
            <div class="col s12">
                <i class="material-icons-outlined theme-primary-text medium">language</i>
                <h5 class="font-weight-900">{{ text_to_display }}</h5>
            </div>
        </div>
        """
        return render_template_string(html_string, text_to_display=self.text_to_display)
```

and in our config.ini:
```ini
[hello_world_ds]
platform = custom_hello_world
text_to_display = Hi there.

[hello_world]
type = custom
data_sources = hello_world_ds
```