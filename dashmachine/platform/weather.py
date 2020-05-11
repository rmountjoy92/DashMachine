"""

##### Weather
Weather is a great example of how you can populate a custom card on the dash. This plugin creates a custom card with weather data from [metaweather.com](https://www.metaweather.com)
```ini
[variable_name]
platform = weather
woeid = 2514815
temp_unit = c
wind_speed_unit = kph
air_pressure_unit = mbar
visibility_unit = km
```
> **Returns:** HTML for custom card

| Variable        | Required | Description                                                                                                                                | Options           |
|-----------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| [variable_name]   | Yes      | Name for the data source.                                                                                                                | [variable_name]   |
| platform          | Yes      | Name of the platform.                                                                                                                    | weather           |
| woeid             | Yes      | woeid of location to use. Go here to get (replace lat and long): https://www.metaweather.com/api/location/search/?lattlong=50.068,-5.316 | url               |
| temp_unit         | No       | The unit to be used for temperature                                                                                                      | c,f               |
| wind_speed_unit   | No       | The unit to be used for wind speed                                                                                                       | kph,mph           |
| air_pressure_unit | No       | The unit to be used for air pressure                                                                                                     | mbar, inHg        |
| visibility_unit   | No       | The unit to be used for visibility                                                                                                       | km,mi             |

> **Working example:**
>```ini
>[variable_name]
>platform = weather
>woeid = 2514815
>
>[custom_card_name]
>type = custom
>data_sources = variable_name
>```

"""

import requests
from flask import render_template_string


class Platform:
    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        # set defaults for omitted options
        if not hasattr(self, "woeid"):
            self.woeid = 2514815
        if not hasattr(self, "temp_unit"):
            self.temp_unit = "c"
        if not hasattr(self, "wind_speed_unit"):
            self.wind_speed_unit = "kph"
        if not hasattr(self, "air_pressure_unit"):
            self.air_pressure_unit = "x"
        if not hasattr(self, "visibility_unit"):
            self.visibility_unit = "km"

        self.html_template = """
        <div class="row">
            <div class="col s6">
                <span class="mt-0 mb-0 theme-primary-text font-weight-700" style="font-size: 36px">{{ value.consolidated_weather[0].the_temp|round(1, 'floor') }}&deg;</h3>
            </div>
            <div class="col s6 right-align">
                <img height="48px" src="https://www.metaweather.com/static/img/weather/{{ value.consolidated_weather[0].weather_state_abbr }}.svg">
            </div>
        </div>
        <div class="row">
            <h6 class="font-weight-900 center theme-muted-text">{{ value.title }}</h6>
        </div>
        <div class="row center-align">
            <i class="material-icons-outlined">keyboard_arrow_down</i>
        </div>
        <div class="row center-align">
            <div class="col s12">
                <div class="collection theme-muted-text">
                    <div class="collection-item"><span class="font-weight-900">Currently: </span>{{ value.consolidated_weather[0].weather_state_name }}</div>
                    <div class="collection-item"><span class="font-weight-900">Min: </span>{{ value.consolidated_weather[0].min_temp|round(1, 'floor') }}&deg; <span class="font-weight-900">Max: </span>{{ value.consolidated_weather[0].max_temp|round(1, 'floor') }}&deg;</div>
                    <div class="collection-item"><span class="font-weight-900">Wind: </span>{{ value.consolidated_weather[0].wind_direction_compass }} at {{ value.consolidated_weather[0].wind_speed|round(1, 'floor') }} {{ wind_speed_unit }}</div>
                    <div class="collection-item"><span class="font-weight-900">Humidity: </span>{{ value.consolidated_weather[0].humidity }}%</div>
                    <div class="collection-item"><span class="font-weight-900">Air Pressure: </span>{{ value.consolidated_weather[0].air_pressure|round(1, 'floor') }} {{ air_pressure_unit }}</div>
                    <div class="collection-item"><span class="font-weight-900">Visibility: </span>{{ value.consolidated_weather[0].visibility|round(1, 'floor') }} {{ visibility_unit }} </div>
                    <div class="collection-item"><span class="font-weight-900">Predictability: </span>{{ value.consolidated_weather[0].predictability }}%</div>
                </div>
            </div>
        </div>
        """

        self.error_template = """
        <div class="row">
            <div class="col s12">
                <span class="theme-failure-text font-weight-900">Check your config. This error was returned: {{ error }}</span>
            </div>
        </div>
        """

    def process(self):
        try:
            value = requests.get(
                f"https://www.metaweather.com/api/location/{self.woeid}"
            ).json()
        except Exception as error:
            return render_template_string(self.error_template, error=error)

        if self.temp_unit.lower() == "f":
            value["consolidated_weather"][0]["the_temp"] = (
                value["consolidated_weather"][0]["the_temp"] * 1.8
            ) + 32
            value["consolidated_weather"][0]["min_temp"] = (
                value["consolidated_weather"][0]["min_temp"] * 1.8
            ) + 32
            value["consolidated_weather"][0]["max_temp"] = (
                value["consolidated_weather"][0]["max_temp"] * 1.8
            ) + 32

        if self.wind_speed_unit.lower() == "mph":
            value["consolidated_weather"][0]["wind_speed"] = (
                value["consolidated_weather"][0]["wind_speed"] * 1.609
            )

        if self.air_pressure_unit.lower() == "inhg":
            value["consolidated_weather"][0]["air_pressure"] = (
                value["consolidated_weather"][0]["air_pressure"] / 33.864
            )

        if self.visibility_unit.lower() == "mi":
            value["consolidated_weather"][0]["visibility"] = (
                value["consolidated_weather"][0]["visibility"] / 1.609
            )

        return render_template_string(
            self.html_template,
            value=value,
            wind_speed_unit=self.wind_speed_unit,
            air_pressure_unit=self.air_pressure_unit,
            visibility_unit=self.visibility_unit,
        )
