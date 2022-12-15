<h1>async_pysimplegui</h1>

![gif-program-demo](https://github.com/sunCelery/async_pysimplegui/blob/main/gifs/program-demo.gif)

<h2>Table of content</h2>

- [Description](#description)
- [Install](#install)
- [Usage](#usage)
- [To Do](#to-do)

## Description ##
This program allows You to do asynchronous requests to the server (which do not block UI),
and also demonstrates that the requests are asynchronous for sure, by comparing with regular synchronous requests.
(which block UI (clock updating) and is fulfilling much slower))

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

- [done] make aihttp request which not block UI
- [done] clean code style, delete global variables
- implement variant of function which uses thread (window.perform_long_operation) method
