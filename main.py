
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

workers = MicroWorkers(workersCount=5)

for x in range(5) :
    workers.AddJob('JobA.%s' % x, jobA, arg=None, onFinished=jobFinished)
    workers.AddJob('JobB.%s' % x, jobB, arg=None, onFinished=jobFinished)
    workers.AddJob('JobC.%s' % x, jobC, arg=None, onFinished=jobFinished)

# Waiting end of all jobs,
while workers.IsWorking :
    sleep(0.100)

