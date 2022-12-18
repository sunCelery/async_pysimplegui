import sys
import asyncio
from pathlib import Path
from datetime import datetime

import aiohttp
import requests
import PySimpleGUI as sg


class WeatherApp:

    def __init__(self, api_key, api_url, cities_):
        with open(Path("images/toggle_button_on.png"), "rb") as toggle_button_on, \
             open(Path("images/toggle_button_off.png"), "rb") as toggle_button_off:
            self.toggle_button_on = toggle_button_on.read()
            self.toggle_button_off = toggle_button_off.read()

        self.APPID = api_key
        self.API_URL = api_url
        self.cities = cities_

        self.window = self.create_window()

    def create_window(self):
        layout = [
            [sg.Text('Show Clock',),
             sg.Push(),
             sg.Button(
                 image_data=self.toggle_button_off,
                 key='toggle_show_time',
                 button_color=(sg.theme_background_color(),
                               sg.theme_background_color()),
                 border_width=0,
                 metadata=False), ],

            [sg.Text(
                key="clock_output",
                size=(30, 1),)],

            [sg.Button(
                "retrieve_weather",
                key="retrieve_weather",
                size=(30, 1), )],

            [sg.Button(
                "async_retrieve_weather",
                key="async_retrieve_weather",
                size=(30, 1),)],

            [sg.Button(
                "retrieve_weather_pysimplegui_thread",
                key="retrieve_weather_pysimplegui_thread",
                size=(30, 1),)],

            [sg.Text(
                key="weather_output",
                size=(30, 12),
                font=("Courier New", 10),)],

            [sg.Button(
                "clear layout",
                key="clear_output",
                size=(20, 1),)],
            ]

        window = sg.Window("Async program", layout, finalize=True)
        return window

    async def show_clock(self, refresh_rate=.01):
        while True:
            if self.window["toggle_show_time"].metadata:
                self.window["clock_output"].update(datetime.now().strftime("%Y %b %d, %X.%f"))
                self.window.refresh()
            await asyncio.sleep(refresh_rate)

    def retrieve_weather(self, city) -> str:
        weather_string = ""
        with requests.Session() as session:
            params = {"q": city, "APPID": self.APPID}
            response = session.get(url=self.API_URL, params=params)
            weather_json = response.json()

            weather = weather_json["weather"][0]["main"]
            temp = weather_json["main"]["temp"]
            weather_string += f"{city: <15}: {int(temp-273.15): 3}°C {weather}\n"

            return weather_string

    async def async_retrieve_weather(self, city) -> str:
        weather_string = ""
        params = {"q": city, "APPID": self.APPID}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.API_URL, params=params) as response:
                weather_json = await response.json()

                weather = weather_json["weather"][0]["main"]
                temp = weather_json["main"]["temp"]
                weather_string += f'{city: <15}: {int(temp - 273.15): 3}°C {weather}\n'

                return weather_string

    def retrieve_weather_pysimplegui_thread(self) -> str:
        """You need no any async function in your program if You use this method"""
        weather_string = ""
        with requests.Session() as session:
            for city in self.cities:
                params = {"q": city, "APPID": self.APPID}
                response = session.get(self.API_URL, params=params)
                weather_json = response.json()

                weather = weather_json["weather"][0]["main"]
                temp = weather_json["main"]["temp"]
                weather_string += f'{city: <15}: {int(temp - 273.15): 3}°C {weather}\n'

            return weather_string

    async def check_events(self, refresh_rate=.01):
        timeout = int(1000 * refresh_rate)  # milliseconds
        responses = []

        while True:

            event, values = self.window.read(timeout)

            match event:

                case "Exit": window.close()

                case sg.WIN_CLOSED: sys.exit()

                case "toggle_show_time":
                    self.window['toggle_show_time'].metadata = not self.window['toggle_show_time'].metadata
                    if self.window['toggle_show_time'].metadata:
                        toggle_image = self.toggle_button_on
                    else:
                        toggle_image = self.toggle_button_off
                    self.window['toggle_show_time'].update(image_data=toggle_image)

                case "retrieve_weather":
                    weather_string = ""
                    for city in self.cities:
                        weather_string += self.retrieve_weather(city)
                        self.window["weather_output"].update(weather_string)
                        self.window.refresh()

                case "async_retrieve_weather":
                    responses = asyncio.gather(
                        *[self.async_retrieve_weather(city) for city in self.cities]
                        )

                case "retrieve_weather_pysimplegui_thread":
                    self.window.perform_long_operation(
                        lambda: self.retrieve_weather_pysimplegui_thread(),
                        "thread_request_fulfilled")

                case "thread_request_fulfilled":
                    try:
                        self.window["weather_output"].update(values[event])
                        self.window.refresh()
                    except UnboundLocalError:
                        pass

                case "clear_output":
                    self.window["weather_output"].update("")
                    self.window["clock_output"].update("")
                    self.window.refresh()

            # printig async_retrieve_weather to weather_output here
            try:
                if responses.result():
                    weather_string = "".join(responses.result())
                    self.window["weather_output"].update(weather_string)
                    responses = []
            except (asyncio.exceptions.InvalidStateError, NameError, AttributeError):
                pass

            await asyncio.sleep(refresh_rate)

    async def run(self):
        tasks = [asyncio.create_task(self.check_events()),
                 asyncio.create_task(self.show_clock()), ]

        for task in tasks:
            await task


if __name__ == "__main__":
    API_URL = "http://api.openweathermap.org/data/2.5/weather"
    cities = ['Moscow', 'Yerevan', 'Tbilisi', 'Nicosia', 'Podgorica', 'Vladivostok',
              'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York', ]

    with open("APPID.txt", "rt") as API_KEY:
        API_KEY = API_KEY.read().strip()

        app = WeatherApp(API_KEY, API_URL, cities)
        asyncio.run(app.run())
