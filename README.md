<h1>async_pysimplegui</h1>

![gif-program-demo](https://github.com/sunCelery/async_pysimplegui/blob/main/gifs/program-demo.gif)

<h2>Table of content</h2>

- [Description](#description)
- [Install](#install)
- [Usage](#usage)
- [To Do](#to-do)

## Description ##

- **reatriev_weather** button - do common synchronous requests to the weather server

- **async_retrieve_weather** button - fulfill asynchronous requests to the server
(which do not block UI and executes much faster)

- **retrieve_weather_pysimplegui_thread** button - make the requests in their own threaded,
as pysimplegui docs proposes (these requests are fast and do not block UI either
like async requests, but at demonstration You can see a delay caused
probably by threading creation)

- **Clock** - demonsrates either or not UI blocking by buttons requests

## Install ##
**To install the app run one of these blocks in linux terminal**

- if poetry:
```
git clone https://github.com/sunCelery/async_pysimplegui && \
cd async_pysimplegui && \
poetry install
```

- elif pip:
```
git clone https://github.com/sunCelery/async_pysimplegui && \
cd async_pysimplegui && \
python -m venv .venv && source .venv/bin/activate && \
python -m pip install --upgrade pip && pip install .
```

## Usage ##
**To launch the app run one of these blocks in terminal**

- if poetry:
```
poetry run python main.py
```
- else:
```
python main.py
```

## To Do ##

- [done] make aiohttp request which not block UI
- [done] clean code style, delete global variables
- [done] implement variant of function which uses thread (window.perform_long_operation) method
