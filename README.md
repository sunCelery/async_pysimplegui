<h1>learning_asyncio</h1>

<h2>Table of content</h2>

- [Description](#description)
- [Install](#install)
- [Usage](#usage)
- [To Do](#to-do)

## Description ##
It's totaly learning project, to learn asyncio in Python


For now:
- the program is not completely asyc, async_weather_request block UI buttons, but not block UI refreshing
- comparing to sync_weather_request which block either UI buttons and UI refreshing

## Install ##
**To install the app run one of these blocks in terminal**

- if poetry and linux:
```
git clone https://github.com/sunCelery/learning_asyncio && \
cd learning_asyncio && \
poetry install
```

- elif pip and linux:
```
git clone https://github.com/sunCelery/learning_asyncio && \
cd learning_asyncio && \
python -m venv .venv && source .venv/bin/activate && \
python -m pip install --upgrade pip && pip install -r requirements.txt
```

## Usage ##
**To launch the app run one of these blocks in terminal**

- if poetry:
```
poetry run main.py
```
- else:
```
python main.py
```k'
```

## To Do ##

- make aihttp request which not block UI
- clean code style, delete global variables (it's totaly draft file for now) (afaik asyncio.gather must be used to retrieve that async function returns)