from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import redis,logging,time,yaml

app = FastAPI()
r = redis.Redis()

with open("config.yaml") as f:
    config = yaml.safe_load(f)




def fixedwindow(pattern,qps):
    key = f"{pattern}{int(time.time())}"
    r.get(key)
    if int(r.incr(key)) < qps:
        flag = True
    else:
        flag = False
    r.expire(key,1)
    return flag 

def slidingwindow(pattern,qps,delta=1):
    """TODO: do this in a pipeline"""
    key = f"{pattern}"
    now = time.time()
    r.zremrangebyscore(key,0,now - delta)
    if r.zcard(key) < qps:
        r.zadd(key,{now:now}) #we only add successful request else our windows always full of shit
        r.expire(key,delta)
        return True
    else:
        return False


def is_ratelimited(_type,pattern,qps):
    if _type == "fixedwindow":
        return fixedwindow(pattern,qps)
    if _type == "slidingwindow":
        return slidingwindow(pattern,qps)


@app.get("/")
async def root():
    rl_type = config["type"]
    if is_ratelimited(rl_type,"/",10):
        return {"message":"Hello World"}
    else:
        return HTMLResponse(status_code=429)

