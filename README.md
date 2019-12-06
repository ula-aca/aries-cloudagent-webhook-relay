# Hyperledger Aries Cloud Agent - Webhook Receiver

The [Hyperledger Aries Cloud Agent - Python (ACA-Py)](https://github.com/hyperledger/aries-cloudagent-python/tree/01fc73be644439fa27ab43089353859f08517ba2) currently requires the ACA-Py controller to host several webhook endpoints in order to receive updates about the agents state as described [here](https://github.com/hyperledger/aries-cloudagent-python/blob/01fc73be644439fa27ab43089353859f08517ba2/AdminAPI.md). This introduces a problem for mobile ACA-Py controller clients since it is not possible to expose such endpoints.

This repository aims to solve this problem 'the dirty way' by placing another component (called Webhook Receiver) in between ACA-Py and the Controller. The Webhook Receiver exposes the required webhook endpoints and records the requests made by ACA-Py. It also exposes an endpoint and websocket interface to get the recorded messages that the Controller call to process the messages.

#### A note about the websocket
Whenever a client opens a websocket connection, **all** in-memory messages that the client has missed so far will be send in the order they came in. (**TODO -> create cli flag to make it optional**) All new messages will be forwarded directly as long as the websocket connection lives. Whenever the connection is broken we'll start writing into memory again until the next time the client connects.


## Setup

### Docker Compose
The `docker-compose.yml` file contains a Alice - Faber test setup where both Alice and Faber have their own Webhook Receiver instance. Just run:
```bash
docker-compose build
docker-compose up -d
# and when you're done
docker-compose down
```

You can now connect to the various components through the following adresses:


**Alice**
Swagger UI: `http://127.0.0.1:8002`
Webhook Receiver (get new messages): `http://127.0.0.1:8080/new_messages`
Webhook Receiver (websocket): `ws://127.0.0.1:8080/ws`

**Faber**
Swagger UI: `http://127.0.0.1:7002`
Webhook Receiver (get new messages): `http://127.0.0.1:7080/new_messages`
Webhook Receiver (websocket): `ws://127.0.0.1:7080/ws`

### Docker
If you prefer a single container version.

```bash
docker build -t webhook-receiver .
docker run -p 8080:8080 webhook-receiver 
```

### Manual
```bash
# make sure you have virtualenv
pip install virtualenv # or pip3 install virtualenv

# create a virtual environment
virtualenv --python=python3.7 ./webhook-receiver-env

# load it
source ./webhook-receiver-env/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Usage
```
usage: webhook-receiver [-h] [-l {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
                        [--api-key API_KEY] [--insecure-mode] [--host HOST]
                        [--port PORT]

collects and cache's aca-py webhook calls until requested by controller.

optional arguments:
  -h, --help            show this help message and exit
  -l {CRITICAL,ERROR,WARNING,INFO,DEBUG}, --log {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        the log level
  --api-key API_KEY     if passed, this will be used as the API key (one will
                        be generated by default).
  --insecure-mode       if passed, no API key will be generated and the --api-
                        key flag will be ignored.
  --host HOST, -H HOST  the host the receiver will run on
  --port PORT, -p PORT  the port the receiver will run on
```

When you run the `webhook-receiver`, it will print the following message:
```bash
INFO - log level: INFO
INFO - both the --api-key and --insecure-mode flags are not provided
INFO - generated api key: 039372a9-cc60-4c71-9fde-b5848a9ac9e2
INFO - ws exposed at: ws://0.0.0.0:8080/ws
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```
Copy th printed address (in this case `http://0.0.0.0:8080`) and pass it to a ACA-Py instance as the `--webhook-url` argument. All webhook requests made by ACA-Py will now be directed towards the webhook-receiver. Your Controller instance can now fetch the messages by calling `http://0.0.0.0:8080/new-messages` or subscribe to the websocket interface at `http://0.0.0.0:8080/ws`. **Please note** that both methods require the `Authorization` request header to be set to the webhook-receivers API key (in this case `55c56521-df27-4284-a71b-04501cd49c5b`).