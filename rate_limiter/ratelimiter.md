# Rate Limiter

## 1. Background & Concepts
Rate Limiter is a strategy used to limit the incoming traffic to a server. Usually, we would like to set an upper limit of how many requests per second the server can handle, as our computing resources are limited.

Rate limiting can be of different type:
* per api
* per server instance

Rate limiter's QPS usually depends on the server capacity as well as the use case of the api.
## 2. Code Demo
```
Require: redis, fastapi,yaml
```

In this directory, sosig provides a simple client-server model with different kind of rate limiter. The allowed QPS is 10 QPS. 

The client makes request to the server in a constant/edgy QPS fashion. In edgyQPS, it makes the bulk of the request at the edge of the second. 

The server has a 2 type of rate limiter:
* fixed window: which would allow requests at the edge of the window to spillover to the next window. The instantenous QPS at the window edge would therefore can exceed the amount allowed
* sliding window: fix the above problem 

## To run (assuming you are in the rate_limiter dir)
```
# install stuff
pip install fastapi[all]
pip install redis pyyaml

#config the config.yaml to the type of rl you want

# in the first terminal
uvicorn server:app

# in the second terminal 
python client.py
```

## Expected behaviour
1. fixed window

there will be traffic at the edge of the window as the window reset every second. The client should show that it can send more than 10 queries. 

2. Sliding window
Even with edgy sending behaviour, the client can only send 10 queries
