import sys
import asyncio
import requests
import PySimpleGUI as sg
from datetime import datetime
from aiohttp import ClientSession


def make_window(theme=None):
    layout = [
        [sg.Text("UI working in Async mode",)],

        [sg.Button("Turn-ON time",
            key="turn_ON_time_button_pressed",
            size=(13, 1),
            )],
        [sg.Button("Turn-OFF time",
            key="turn_OFF_time_button_pressed",
            size=(13, 1),
            )],
        [sg.Text("output: ",
            key="output",
            size=(30, 1),
            )],

        [sg.Button("ASYNC Retrieve weather",
            key="async_retrieve_weather_button_pressed",
            size=(30, 1),
            )],
        [sg.Text("async weather: ",
            key="async_weather_output",
            size=(30, 13),
            font=("Courier New", 10),
            )],

        [sg.Button("SYNC Retrieve weather",
            key="sync_retrieve_weather_button_pressed",
            size=(30, 1),
            )],
        [sg.Text("sync weather: ",
            key="sync_weather_output",
            size=(30, 13),
            font=("Courier New", 10),
            )],

        [sg.Button("clear Output",
            key="clear_output",
            size=(20, 1),
            )],

    ]

    window = sg.Window('Async program', layout, finalize=True)

    return window


def get_weather(Window, url, city):
    global weather_string

    with requests.Session() as session:
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
        response = session.get(url, params=params)
        weather_json = response.json()
        weather_string += f'{city: <15}: {weather_json["weather"][0]["main"]}\n'


async def async_get_weather(window, url, city):
    global weather_string

    async with ClientSession() as session:
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            weather_string += f'{city: <15}: {weather_json["weather"][0]["main"]}\n'



async def show_time(window, refresh_rate=.01):
    global flag
    flag = None
    while True:
        if flag == "show time":
            print("[ show-time-loop ]")
            window["output"].update(datetime.now().strftime("%Y %b %d, %X.%f"))
            window.refresh()
        await asyncio.sleep(refresh_rate)


async def read_events(window, refresh_rate=.1):
    global event
    while True:
        event = window.read(timeout=10)[0]
        print("[ read-event-loop ]")
        await asyncio.sleep(refresh_rate)


async def check_events(window, refresh_rate=.1):
    global flag
    global event
    global weather_tasks, cities, weather_string
    url = 'http://api.openweathermap.org/data/2.5/weather'

    while True:

        if event == sg.WIN_CLOSED or event == "Exit":
            flag = "exit"
            print("1st if == Quit")
            window.close()
            sys.exit()

        if event == "turn_ON_time_button_pressed":
            flag = "show time"
            print("2nd if == turn_ON_time_button_pressed\n")

        if event == "turn_OFF_time_button_pressed":
            flag = "dont show time"
            print("3d if == turn_OFF_time_button_pressed\n")

        if event == "async_retrieve_weather_button_pressed":
            weather_string = ""
            print("4d if == async_retrieve_weather_button_pressed")
            for city in cities:
                await async_get_weather(window, url, city)
                window["async_weather_output"].update(weather_string)
                window.refresh()

        if event == "sync_retrieve_weather_button_pressed":
            weather_string = ""
            print("5d if == sync_retrieve_weather_button_pressed")
            for city in cities:
                get_weather(window, url, city)
                window["sync_weather_output"].update(weather_string)
                window.refresh()

        if event == "clear_output":
            window["async_weather_output"].update("")
            window["sync_weather_output"].update("")
            window.refresh()

        print("[ check-events-loop ]")
        await asyncio.sleep(refresh_rate)


async def main():
    global event
    global cities, weather_string

    flag = None
    window = make_window()
    url = 'http://api.openweathermap.org/data/2.5/weather'
    cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
              'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York']

    task_read_events = asyncio.create_task(read_events(window))
    task_check_events = asyncio.create_task(check_events(window))
    task_show_time = asyncio.create_task(show_time(window))

    await task_read_events
    await task_check_events
    await task_show_time


if __name__ == "__main__":
    asyncio.run(main())  # Event loop
