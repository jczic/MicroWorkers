### MicroWorkers is a class that easily manages a pool of threads to optimise simultaneous jobs and jobs endings, for MicroPython (used on ESP32 and [Pycom](http://www.pycom.io) modules)

Very easy to integrate and very light with one file only :
- `"microWorkers.py"`

Simple but effective :
- Use it to create a multitasking jobs container
- Add jobs without blocking your main code
- Be alerted by an event when a job has finished

### Using *microWorkers* class :

| Name  | Function |
| - | - |
| Constructor | `workers = MicroWorkers(workersCount, workersStackSize=0)` |
| Adds a job | `workers.AddJob(name, function, arg=None, onFinished=None)` |
| Gets workers count | `workers.Count()` |

### Simple example :
```python
from microWorkers import MicroWorkers
from time		  import sleep

def sleepJob(jobName, jobArg) :
	sleep(10)
	return True

# workersStackSize must be greater than or equal to 4096 (4KB)
# it can be equal to 0 to use the default stack size
workers = MicroWorkers(workersCount=5, workersStackSize=10*1024)

for i in range(5) :
	workers.AddJob('Job %s' % i, sleepJob)
```

### Example of using multiple jobs (with finished event) :
```python
from microWorkers import MicroWorkers
from time		  import sleep

print()

def jobTest1(jobName, jobArg) :
	sleep(1)
	return '%s:OK:1s' % jobName

def jobTest2(jobName, jobArg) :
	sleep(3)
	return '%s:OK:3s' % jobName

def jobTest3(jobName, jobArg) :
	sleep(5)
	return '%s:OK:5s' % jobName

def jobFinished(jobName, jobArg, jobResult) :
	print('Job %s finished (%s)' % (jobName, jobResult))

workers = MicroWorkers(workersCount=3)

for x in range(5) :
	workers.AddJob('Test1', jobTest1, arg=None, onFinished=jobFinished)
	workers.AddJob('Test2', jobTest2, arg=None, onFinished=jobFinished)
	workers.AddJob('Test3', jobTest3, arg=None, onFinished=jobFinished)
```


### By JC`zic for [HC²](https://www.hc2.fr) ;')

*Keep it simple, stupid* :+1:
