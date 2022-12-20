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
                size=(48, 1), )],

            [sg.Button(
                "retrieve_weather_async",
                key="retrieve_weather_async",
                size=(48, 1),)],

            [sg.Button(
                "retrieve_weather_thread",
                key="retrieve_weather_thread",
                size=(48, 1),)],

            [sg.Text(
                key="weather_header",
                size=(45, 1),
                font=("Courier New", 10, "bold"), )],

            [sg.Text(
                key="weather_output",
                size=(45, 12),
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
            params = {"q": city, "units": "metric", "APPID": self.APPID}
            response = session.get(url=self.API_URL, params=params)
            weather_json = response.json()

            weather = weather_json["list"][0]["weather"][0]["main"]
            temperature = round(weather_json["list"][0]["main"]["temp"])

            weather_tom = weather_json["list"][8]["weather"][0]["main"]
            temperature_tom = round(weather_json["list"][8]["main"]["temp"])

            weather_string += f'{city[:15]:<15}: {temperature:>3}°C {weather:<6} -> ' \
                              f'{temperature_tom:>3}°C {weather_tom:<6}\n'

            return weather_string

    async def retrieve_weather_async(self, city) -> str:
        weather_string = ""
        params = {"q": city, "units": "metric", "APPID": self.APPID}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.API_URL, params=params) as response:
                weather_json = await response.json()

                weather = weather_json["list"][0]["weather"][0]["main"]
                temperature = round(weather_json["list"][0]["main"]["temp"])

                weather_tom = weather_json["list"][8]["weather"][0]["main"]
                temperature_tom = round(weather_json["list"][8]["main"]["temp"])

                weather_string += f'{city[:15]:<15}: {temperature:>3}°C {weather:<6} -> ' \
                                  f'{temperature_tom:>3}°C {weather_tom}\n'

                return weather_string

    def retrieve_weather_thread(self) -> str:
        """You need no any async function in your program if You use this method"""
        weather_string = ""
        with requests.Session() as session:
            for city in self.cities:
                params = {"q": city, "units": "metric", "APPID": self.APPID}
                response = session.get(self.API_URL, params=params)
                weather_json = response.json()

                weather = weather_json["list"][0]["weather"][0]["main"]
                temperature = round(weather_json["list"][0]["main"]["temp"])

                weather_tom = weather_json["list"][8]["weather"][0]["main"]
                temperature_tom = round(weather_json["list"][8]["main"]["temp"])

                weather_string += f'{city[:15]:<15}: {temperature:>3}°C {weather:<6} -> ' \
                                  f'{temperature_tom:>3}°C {weather_tom}\n'

            return weather_string

    async def check_events(self, refresh_rate=.01):
        timeout = 1  # milliseconds, duration of blocking window.read() method call
        responses = []

        while True:

            event, values = self.window.read(timeout)

            match event:

                case "Exit":
                    window.close()

                case sg.WIN_CLOSED:
                    sys.exit()

                case "toggle_show_time":
                    self.window['toggle_show_time'].metadata = not(
                        self.window['toggle_show_time'].metadata)
                    if self.window['toggle_show_time'].metadata:
                        toggle_image = self.toggle_button_on
                    else:
                        toggle_image = self.toggle_button_off
                    self.window['toggle_show_time'].update(image_data=toggle_image)

                case "retrieve_weather":
                    self.window["weather_header"].update(
                        f"{'City':^15}: {'Now':^12} -> {'24H later:':^12}")
                    weather_string = ""
                    for city in self.cities:
                        weather_string += self.retrieve_weather(city)
                        self.window["weather_output"].update(weather_string)
                        self.window.refresh()

                case "retrieve_weather_async":
                    responses = asyncio.gather(
                        *[self.retrieve_weather_async(city) for city in self.cities]
                        )

                case "retrieve_weather_thread":
                    self.window.perform_long_operation(
                        lambda: self.retrieve_weather_thread(),
                        "retrieve_weather_thread_fulfilled")

                case "retrieve_weather_thread_fulfilled":
                    try:
                        self.window["weather_header"].update(
                            f"{'City':^15}: {'Now':^12} -> {'24H later:':^12}")
                        self.window["weather_output"].update(values[event])
                        self.window.refresh()
                    except UnboundLocalError:
                        pass

                case "clear_output":
                    self.window["clock_output"].update("")
                    self.window["weather_output"].update("")
                    self.window["weather_header"].update("")
                    self.window.refresh()

            # printing retrieve_weather_async
            try:
                if responses.result():
                    self.window["weather_header"].update(
                        f"{'City':^15}: {'Now':^12} -> {'24H later:':^12}")
                    weather_string = "".join(responses.result())
                    self.window["weather_output"].update(weather_string)
                    responses = []
            except (asyncio.exceptions.InvalidStateError,
                    NameError, AttributeError):
                pass

            await asyncio.sleep(refresh_rate)

    async def run(self):
        tasks = [asyncio.create_task(self.check_events()),
                 asyncio.create_task(self.show_clock()), ]

        for task in tasks:
            await task


if __name__ == "__main__":
    API_URL = "http://api.openweathermap.org/data/2.5/forecast"
    cities = ['Moscow', 'Yerevan', 'Tbilisi', 'Nicosia', 'Podgorica', 'Petropavlovsk-Kamchatsky',
              'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York', ]

    with open("APPID.txt", "rt") as API_KEY:
        API_KEY = API_KEY.read().strip()

        app = WeatherApp(API_KEY, API_URL, cities)
        asyncio.run(app.run())
