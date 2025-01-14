# async-example-py

This project is a simple example HTTP API server built with FastAPI for demonstrating how to apply asynchronous
IO in a standard Python project.

## Prerequisites

You need to have the following tools installed:

- [direnv](https://direnv.net/)
- [nix](https://nix.dev/)
- [nix-direnv](https://nix.dev/nix-direnv/)

## Getting Started

To get started, clone the repository and run the following commands:

```bash
git clone https://github.com/your-username/async-example-py.git
cd async-example-py
```

Having all the prerequisites installed, you can run the following command to start the development environment:

```bash
direnv allow
```

This will install all the dependencies in an isolated environment, and you can start the API server by running:

```bash
start
```

which will start the FastAPI server on port 8000, running the uvicorn server.

You can also run the API in Docker by running:

```bash
docker-build
docker-run
```

## Key Takeaways

We use the following libraries:

- The `httpx` library is used to make HTTP requests asynchronously.
- The `fastapi` library is used to build the FastAPI server.
- The `pytest` library is used to run the tests.
- The `black` library is used to format the code.
- The `flake8` library is used to lint the code.

Under the hood, we are powered by the following technologies:

- [asyncio](https://docs.python.org/3/library/asyncio.html) is the standard library for asynchronous IO in Python.
- [ASGI](https://asgi.readthedocs.io/en/latest/) (`Asynchronous Server Gateway Interface`), a standard interface between web servers and async web applications and servers.
- [Uvicorn](https://www.uvicorn.org/) is a lightning-fast ASGI server implementation, using [uvloop](https://github.com/MagicStack/uvloop) replacing the default asyncio event loop and [httptools](https://github.com/MagicStack/httptools) replacing the default asyncio parser.

## Exercises

- Use [magnum](https://github.com/Kludex/mangum) or [AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter) to run the FastAPI server in a Lambda environment.
- Use [aioboto3](https://github.com/terricain/aioboto3) to make asynchronous AWS API requests.
- Use [SQLAlchemy Asynchronous I/O (asyncio) Extention](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) to make asynchronous database requests.
- Use [redis-py](https://redis-py.readthedocs.io/en/stable/examples/asyncio_examples.html) to make asynchronous Redis requests.

## Findings

- `aioboto3core` and hence `aioboto3` are not integrated with `httpx` yet as of writing this [(issue)](https://github.com/aio-libs/aiobotocore/pull/1085)
- Although the python asyncio idiom `async with` seems to good for creating a asyncio whatever client/session/etc per a API request, it is not always necessary. You usually create a session/client/etc and cache it for the duration of the application. See [this](https://github.com/terricain/aioboto3/issues/343) for example.
