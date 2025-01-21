# async-example-py

This project is a simple example HTTP API server built with FastAPI for demonstrating how to apply asynchronous
IO in a standard Python project.

See [main.py](src/main.py) for the main entry point, and [services/external_api.py](src/services/external_api.py) for the service that makes HTTP requests to an external API (https://jsonplaceholder.typicode.com).

ToC:

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Exercises](#exercises)
- [Findings](#findings)
- [Key Takeaways](#key-takeaways)

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

## Exercises

- Use [magnum](https://github.com/Kludex/mangum) or [AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter) to run the FastAPI server in a Lambda environment.
- Use [aioboto3](https://github.com/terricain/aioboto3) to make asynchronous AWS API requests.
- Use [SQLAlchemy Asynchronous I/O (asyncio) Extention](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) to make asynchronous database requests.
- Use [redis-py](https://redis-py.readthedocs.io/en/stable/examples/asyncio_examples.html) to make asynchronous Redis requests.

## Findings

- `aioboto3core` and hence `aioboto3` are not integrated with `httpx` yet as of writing this [(issue)](https://github.com/aio-libs/aiobotocore/pull/1085)
- Although the python asyncio idiom `async with` seems to good for creating a asyncio whatever client/session/etc per a API request, it is not always necessary. You usually create a session/client/etc and cache it for the duration of the application. See [this](https://github.com/terricain/aioboto3/issues/343) for example.

## Key Takeaways

We can use `fastapi` to build an async API server. By default, `fastapi` uses `uvicorn` as the ASGI server, which in turn uses `asyncio` and `uvloop` to handle the async IO.

As it's based on `asyncio`, we can use other async libraries that are compatible with `asyncio` such as `aioboto3`, `aioredis`, `sqlalchemy-asyncio`, etc.

- [Useful Libraries](#useful-libraries)
- [How Async IO Works in General](#how-async-io-works-in-general)
  - [System Call Evolution](#system-call-evolution)
  - [How Python's asyncio Uses These](#how-pythons-asyncio-uses-these)
  - [Language Runtimes](#language-runtimes)

### Useful Libraries

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

### How Async IO Works in General

Asynchronous I/O allows programs to handle multiple I/O operations concurrently without using multiple threads or processes. Here's how it works under the hood:

#### System Call Evolution

1. **select/poll (Traditional)**
   - Oldest multiplexing system calls
   - Maintains a list of file descriptors to monitor
   - Limited scalability (O(n) scanning of descriptors)
   - Still used in some legacy systems and for broad compatibility

2. **epoll (Linux 2.5.44+)**
   - Modern event notification system
   - O(1) performance for descriptor monitoring
   - Edge-triggered or level-triggered events
   - Used by Node.js, Python asyncio (default on Linux) (See [this](https://dev.to/skywind3000/performance-asyncio-vs-gevent-vs-native-epoll-bnl) for how asyncio+uvloop is comparable to native epoll)
   - Better scalability for many connections

3. **kqueue (BSD/macOS)**
   - BSD's equivalent to epoll
   - Similar performance characteristics
   - Used by Python asyncio on BSD/macOS systems

4. **io_uring (Linux 5.1+)**
   - Newest async I/O interface
   - True asynchronous operations (zero-copy)
   - Submission and completion queue rings
   - Better performance for disk I/O
   - Growing adoption in modern applications

#### How Python's asyncio Uses These

Python's asyncio and uvloop use these system calls as follows:

- Default asyncio event loop uses epoll on Linux, kqueue on BSD/macOS
- uvloop (used by Uvicorn) optimizes this further with a [Cython](https://cython.org/) implementation
- The event loop monitors file descriptors for I/O readiness
- When I/O is ready, corresponding coroutines are awakened

Example flow:
```python
async def fetch_url(url):
    # Under the hood:
    # 1. Socket is created
    # 2. Added to epoll/kqueue/etc monitoring
    # 3. Coroutine suspended until data ready
    # 4. System call notifies event loop
    # 5. Coroutine resumed
    async with httpx.AsyncClient() as client:
        return await client.get(url)
```

#### Language Runtimes

Many modern language runtimes use these system calls:
- Node.js: Uses [libuv](https://github.com/libuv/libuv) (epoll/kqueue)
- Rust/Tokio: Configurable (epoll/kqueue/io_uring)
- Go: Custom runtime with netpoller (epoll/kqueue) (See [this](https://qiita.com/takc923/items/de68671ea889d8df6904) for how Go's netpoller works within the Go runtime)
- Python/asyncio: epoll/kqueue via event loop

This low-level multiplexing enables the high-level async/await syntax we use in our application code.
