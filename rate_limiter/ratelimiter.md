# Rate Limiter

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
