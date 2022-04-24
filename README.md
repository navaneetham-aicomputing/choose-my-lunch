<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Description](#description)
* [Technologies](#technologies)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Testing](#testing)
  * [Contributing](#contributing)


<!-- ABOUT THE PROJECT -->
## Description

`my_lunch` - base description


### Technologies
This microservice is written with Python 3.9.

A bunch of awesome packages are used:
* [fastapi](https://fastapi.tiangolo.com/) - high-performance web-framework
* [uvicorn](https://github.com/encode/uvicorn) -  the lightning-fast ASGI server


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

To run this locally you'll need [Python 3.9](https://www.python.org/downloads/),
[Docker](https://www.docker.com/products/docker-desktop) and [Poetry](https://python-poetry.org/docs/)
installed on your computer.


### Build & run docker image

```sh
$ cp env.compose.example .env.compose
$ docker build -t my_menu:0.1 .
$ docker-compose up
```

### Access APIs

Access http://127.0.0.1:8080/docs 



