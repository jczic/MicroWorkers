
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
