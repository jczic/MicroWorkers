### MicroWorkers is a class that easily manages a pool of threads to optimise simultaneous jobs and jobs endings, for MicroPython (used on ESP32 and [Pycom](http://www.pycom.io) modules)

![HC²](hc2.png "HC²")

Very easy to integrate and very light with one file only :
- `"microWorkers.py"`

Simple but effective :
- Use it to create a multitasking jobs container
- Add jobs without blocking your main code
- Be alerted by an event when a job has finished

### Using *microWorkers* class :

| Description  | Function |
| - | - |
| Constructor | `workers = MicroWorkers(workersCount, workersStackSize=None)` |
| Adds a job | `workers.AddJob(name, function, arg=None, onFinished=None)` |

| Description  | Property |
| - | - |
| Returns workers count | `workers.Count` |
| Returns emaining jobs count | `workers.JobsInQueue` |
| Returns jobs in process count  | `workers.JobsInProcess` |
| Returns `True` if is in working | `workers.IsWorking` |

### Simple example :
```python
from microWorkers import MicroWorkers
from time         import sleep

def sleepJob(jobName, jobArg) :
	sleep(10)
	return True

workers = MicroWorkers(workersCount=5)

for i in range(5) :
	workers.AddJob('Job %s' % i, sleepJob)
```

### Example of using multiple jobs (with finished event) :
```python
from microWorkers import MicroWorkers
from time         import sleep

print()

def jobA(jobName, jobArg) :
    sleep(1)
    return '%s:OK:1s' % jobName

def jobB(jobName, jobArg) :
    sleep(2)
    return '%s:OK:2s' % jobName

def jobC(jobName, jobArg) :
    sleep(3)
    return '%s:OK:3s' % jobName

def jobFinished(jobName, jobArg, jobResult) :
    print('Job %s finished (%s)' % (jobName, jobResult))

# workersStackSize must be greater than zero
# it can be None to use the default stack size
workers = MicroWorkers(workersCount=5, workersStackSize=10*1024)

for x in range(5) :
    workers.AddJob('JobA.%s' % x, jobA, arg=None, onFinished=jobFinished)
    workers.AddJob('JobB.%s' % x, jobB, arg=None, onFinished=jobFinished)
    workers.AddJob('JobC.%s' % x, jobC, arg=None, onFinished=jobFinished)

# Waiting end of all jobs,
while workers.IsWorking :
    sleep(0.100)
```


### By JC`zic for [HC²](https://www.hc2.fr) ;')

*Keep it simple, stupid* :+1:
