import sys
import asyncio
import aiohttp
import requests
import PySimpleGUI as sg
from datetime import datetime


def make_window(toggle_button_off):
    layout = [
        [sg.Text('Show Clock',),
         sg.Push(),
         sg.Button(
             image_data=toggle_button_off,
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
            size=(30, 1),)],

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

    window = sg.Window('Async program', layout, finalize=True)
    return window


async def show_clock(window, refresh_rate=.01):
    while True:
        if window['toggle_show_time'].metadata:
            # print("[ show-time-loop ]")
            window["clock_output"].update(datetime.now().strftime("%Y %b %d, %X.%f"))
            window.refresh()
        await asyncio.sleep(refresh_rate)


def retrieve_weather(url, city, APPID) -> str:
    weather_string = ""
    with requests.Session() as session:
        params = {"q": city, "APPID": APPID}
        response = session.get(url=url, params=params)
        weather_json = response.json()

        weather = weather_json["weather"][0]["main"]
        temp = weather_json["main"]["temp"]
        weather_string += f'{city: <15}: {int(temp-273.15): 3}°C {weather}\n'

        return weather_string


async def async_retrieve_weather(url, city, APPID) -> str:
    weather_string = ""
    params = {"q": city, "APPID": APPID}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()

            weather = weather_json["weather"][0]["main"]
            temp = weather_json["main"]["temp"]
            weather_string += f'{city: <15}: {int(temp - 273.15): 3}°C {weather}\n'

            return weather_string


def retrieve_weather_pysimplegui_thread(url, cities, APPID) -> str:
    """You need no any async function in your program if You use this method"""
    weather_string = ""
    with requests.Session() as session:
        for city in cities:
            params = {"q": city, "APPID": APPID}
            response = session.get(url, params=params)
            weather_json = response.json()

            weather = weather_json["weather"][0]["main"]
            temp = weather_json["main"]["temp"]
            weather_string += f'{city: <15}: {int(temp - 273.15): 3}°C {weather}\n'

        return weather_string


async def check_events(window,
                       toggle_button_on,
                       toggle_button_off,
                       cities,
                       APPID,
                       url,
                       refresh_rate=.01):

    timeout = 10  # milliseconds

    while True:

        event, values = window.read(timeout)

        match event:

            case "Exit": window.close()

            case sg.WIN_CLOSED: sys.exit()

            case "toggle_show_time":
                window['toggle_show_time'].metadata = not window['toggle_show_time'].metadata
                toggle_image = toggle_button_on if window['toggle_show_time'].metadata else toggle_button_off
                window['toggle_show_time'].update(image_data=toggle_image)

            case "retrieve_weather":
                weather_string = ""
                for city in cities:
                    weather_string += retrieve_weather(url, city, APPID)
                    window["weather_output"].update(weather_string)
                    window.refresh()

            case "async_retrieve_weather":
                responses = asyncio.gather(
                    *[async_retrieve_weather(url, city, APPID) for city in cities]
                    )

            case "retrieve_weather_pysimplegui_thread":
                window.perform_long_operation(
                    lambda: retrieve_weather_pysimplegui_thread(url, cities, APPID),
                    "thread_request_fulfilled")

            case "thread_request_fulfilled":
                try:
                    window["weather_output"].update(values[event])
                    window.refresh()
                except UnboundLocalError:
                    pass

            case "clear_output":
                window["weather_output"].update("")
                window["clock_output"].update("")
                window.refresh()

        # printig async_retrieve_weather to weather_output here
        try:
            if responses.result():
                weather_string = "".join(responses.result())
                window["weather_output"].update(weather_string)
                responses = []
        except (asyncio.exceptions.InvalidStateError, NameError, AttributeError):
            pass

        # print("[ check-events-loop ]")
        await asyncio.sleep(refresh_rate)


async def main():
    APPID = "c0c7c0a9652c9767d76fe79685f3e008"
    url = "http://api.openweathermap.org/data/2.5/weather"

    with open("toggle_button_on.txt") as toggle_button_on, \
         open("toggle_button_off.txt") as toggle_button_off:
        toggle_button_on = toggle_button_on.read()
        toggle_button_off = toggle_button_off.read()

        window = make_window(toggle_button_off)
        cities = ['Moscow',
                  'Yerevan',
                  'Tbilisi',
                  'Nicosia',
                  'Podgorica',
                  'Vladivostok',
                  'Beijing',
                  'Delhi',
                  'Istanbul',
                  'Tokyo',
                  'London',
                  'New York', ]

        tasks = [
            asyncio.create_task(
                check_events(
                    window,
                    toggle_button_on, toggle_button_off,
                    cities, APPID, url)),

            asyncio.create_task(
                show_clock(
                    window))
        ]

        for task in tasks:
            await task


if __name__ == "__main__":
    asyncio.run(main())  # Event loop
