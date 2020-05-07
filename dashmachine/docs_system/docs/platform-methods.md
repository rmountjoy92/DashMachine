### Platform Methods
These are the various methods DM will call on your Platform. Some are optional, some are required.

<div class="divider"></div>

##### `def docs(self):` (*required*)

This is the function DM calls to get the metadata about your plaform. This is what DM uses to generate the documentation and options in the gui forms. It is very important that this information is correct.

<div class="divider"></div>

##### `def __init__(self, *args, **kwargs):` (*required*)
This is the initialization function. This should be reserved for setting up the platform's configuration. NOTE: this is not where you call APIs, as this code is run every time DM initializes your 'Platform' class (e.g. to pull documentation, etc).

<div class="divider"></div>

##### `def process(self):` (*required*)
This is the function that is ran when the web client requests information from this platform (e.g. when the dashboard is loaded) this is where you call APIs, or whatever you're doing to get data.

<div class="divider"></div>

##### `def on_startup(self):` (*optional*)
This function is run when DM starts up, this is a great place for registering API routes or installing dependencies.
