<h1>async_pysimplegui</h1>

![gif-program-demo](https://github.com/sunCelery/async_pysimplegui/blob/main/gifs/program-demo.gif)

<h2>Table of content</h2>

- [Description](#description)
- [Install](#install)
- [Usage](#usage)
- [To Do](#to-do)

## Description ##

**Program shows weather and next day forcast for given cites**

**It's also demonstrates how long it takes time for different methods of request**

- **reatriev_weather** button - do common synchronous requests to the weather server

- **retrieve_weather_async** button - fulfill asynchronous requests to the server
(which do not block UI and executes much faster)

- **retrieve_weather_thread** button - make the requests in their own threaded,
as pysimplegui docs proposes (these requests are fast and do not block UI either
like async requests, but at demonstration You can see a delay caused
probably by threading creation (or even more probably becayse this method need
to be used inside common synchronous loop over asynchronous like here))

- **Clock** - demonsrates either or not UI to be blocked by defferent methods

## Install ##
**Linux**
**To install the app run one of these blocks in terminal:**

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

**Windows:**
**after you clone repository go to the folder and run command in Your terminal:**

```
py -m venv venv && venv\Scripts\activate ^
py -m pip install --upgrade pip && pip install .
```
<em>probably instead 'py' You should type 'python'</em>

## Usage ##
**You need 'APPID.txt' file with Your API-KEY in there for program to work**

**To launch the app run one of these blocks in terminal**

**Linux**
- if poetry:
```
poetry run python main.py
```
- else:
```
python main.py
```
**Windows**
```
python main.py
```

## To Do ##

- [done] make aiohttp request which not block UI
- [done] clean code style, delete global variables
- [done] implement variant of function which uses thread (window.perform_long_operation) method
- [done] lead to OOP
