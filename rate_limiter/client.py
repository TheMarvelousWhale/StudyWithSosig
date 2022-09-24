from collections import defaultdict
import requests
import functools
import time
import math 
import yaml 

target = 'http://127.0.0.1:8000'

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Query {value} times in {run_time:.4f} secs\nQPS = {value/run_time:.4f}")
        return value
    return wrapper_timer

class Client:
    def __init__(self):
        self.status_counter = defaultdict(int)
    

    def get(self):
        x = requests.get(target)
        self.status_counter[x.status_code] += 1 
        return 1

    def tab(self):
        print(f"call resutls:")
        for k,v in self.status_counter.items():
            print(f"\t Code {k}: {v} times")
    
    @timer
    def get_many(self,n):
        for _ in range(n):
            self.get()
        self.tab()
        return n
        
        
    def constantQPS(self,qps,n):
        """max qps 400"""
        dur = 1/qps
        for _ in range(n):
            start_time = time.perf_counter() 
            self.get()
            end_time = time.perf_counter()
            run_time = end_time - start_time
            if dur > run_time:
                time.sleep(dur-run_time) #appx time it needs to call 1 get
        self.tab()
        return n

    def edgyQPS(self,qps,n):
        #wait till 0.95 of a sec then start
        for _ in  range(math.ceil(n/qps)):
            now = time.time()
            edge = 0.05
            dur = math.ceil(time.time())-now-edge
            if dur > 0:
                time.sleep(dur)
            for _ in range(qps):
                self.get()
        self.tab()


c = Client()
rl_type = config["type"]
if rl_type == "fixedwindow":
    c.edgyQPS(100,100)
elif rl_type == "slidingwindow":
    c.edgyQPS(100,100)
