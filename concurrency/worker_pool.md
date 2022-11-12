# Worker Pool

So you have a large number (N) of similar tasks (callables, functions, routines,...) to run and it's not very sensible to run them sequentially since each of them can be run independent of each other. What are some options? 

1. Batching: 

By running a controlled number of parallel threads at the same time, we can run the task much faster. A simple example is:

```
i = 0
while i < N
    upperBound = min(i,N)
    batch = tasks[i:upperbound]

    // spawn #batch number of processes/thread to run the task 

    // wait for all processes/thread to finish * 

    i += batch_size
```

Pros: 
* simple, supported in most languages due to easy concurrency mechanism
* time gain is `$(batch size)`, this is also the max concurrency

Cons:
* if one task takes too long, the batch will be slowed down before we can process next task

As can be seen, the cons is problematic in certain situations. And hence came the second solution

2. Worker Pool

In this design, we have the x number of workers in the pool who is ready to execute to the task. As long as they finish executing the task, they are returned to the pool, ready to take on the next task. In this case, even if one worker is stucked, we still have the other workers available for the remaining tasks. 

The pattern involves:
* creating a pool of worker
* create a queue of jobs to be run
* submit the job to the job queue, and the job is dispatched to the worker pool. 
    * if workers are available, immediately work on the job, return to pool once done
    * otherwise job is queued 
* wait for all workers to finish/timeout 
* do something useful with the results 

There is a few things to notes on the job:
* if the job need any arguments, these should be contained in a closure
* if the result needs to be aggregated, the results data struct should be concurrent-write safe


In python this is ridiculously simple: 
```
with Pool(processes=4) as pool: 
    result = pool.map($taskName, $theIterables)
```

Although there is some issues (memory management, efficiency, etc) that need you to read the [docs](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool) overall it's a simple thing. 


For golang, a simple implementation (assume you know what is a golang channel) to collect 1000 cat pics is 
```
type Job func() 
func worker(jobs chan Job) {
    for j := range Jobs {
        j()
    }
}

func GetCatPic(url string) bool {
    panic("implement me")
}

func GetAllCatPicURLs() []string {
    panic("implement me")
}

func main() {
    catPicURLs := GetAllCatPicURLs()

    numWorkers :=5 

    jobs:= make(chan Job, len(catPicURLs))
    results := make(chan bool, len(catPicURLs))

    //dispatch 
    for w:= 0; w < numWorkers; w++ {
        go worker(jobs)
    }

    //submit job 
    for _, url := range catPicUrls {
        _url = url //rmb closure for this argument 
        jobs <- func() {
            results <- GetCatPic(_url)
        }
    }

    close(jobs)
    for res in results {
        //do something
    }

}

```

Note:
* i conveniently use the results chan as a mechanism to wait for all workers to complete as it is blocking. For completeness please use a waitgroup. 

For actual use case, we can use `https://github.com/gammazero/workerpool` as it has close to 1k stars. It has these features on top of my implementation:
* Dynamic Pool Size
* Waiting Task Queue 
* Pause
* Graceful (and configurable) shutdown 
* And some other smaller features

In extreme cases, when worker needs to be paced, the author also provides a separate pacer package to do that. 


Pros:
* much more flexibility and optimal

Cons:
* need more advanced concurrency control mechanism
* need to manage memory well 