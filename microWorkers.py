"""
The MIT License (MIT)
Copyright © 2019 Jean-Christophe Bos & HC² (www.hc2.fr)
"""

import _thread

class MicroWorkersException(Exception) :
    pass

class MicroWorkers :

    # ============================================================================
    # ===( Thread )===============================================================
    # ============================================================================

    def _workerThreadFunc(self, arg) :
        threadID = _thread.get_ident()
        print('MicroWorkers: Thread #%s created' % threadID)
        while True :
            self._workersLock.acquire()
            try :
                jobName, jobFunc, jobArg, jobCBFunc = self._jobs.pop(0)
            except :
                jobFunc = None
                print('MicroWorkers: Thread #%s waiting for a job...' % threadID)
                self._workersLock.acquire()
            self._workersLock.release()
            if jobFunc :
                with self._jobsLock :
                    self._jobsPrcCount += 1
                print('MicroWorkers: Job %s starts in thread #%s' % (jobName, threadID))
                try :
                    jobResult = jobFunc(jobName, jobArg)
                    print('MicroWorkers: Job %s finished successfully in thread #%s' % (jobName, threadID))
                except Exception as ex :
                    jobResult = None
                    print('MicroWorkers: Job %s raises an exception in thread #%s : %s' % (jobName, threadID, ex))
                if jobCBFunc :
                    try :
                        jobCBFunc(jobName, jobArg, jobResult)
                    except Exception as ex :
                        print('MicroWorkers: Finished callback of job %s raises an exception in thread #%s : %s' % (jobName, threadID, ex))
                with self._jobsLock :
                    self._jobsPrcCount -= 1

    # ============================================================================
    # ===( Constructor )==========================================================
    # ============================================================================

    def __init__(self, workersCount, workersStackSize=None) :
        self._workersCount = workersCount
        self._workersLock  = _thread.allocate_lock()
        self._jobsLock     = _thread.allocate_lock()
        self._jobsPrcCount = 0
        self._jobs         = [ ]
        originalStackSize  = None
        if not isinstance(workersCount, int) or workersCount <= 0 :
            raise MicroWorkersException('"workersCount" must be an integer greater than zero.')
        if workersStackSize is not None :
            if not isinstance(workersStackSize, int) or workersStackSize <= 0 :
                raise MicroWorkersException('"workersStackSize" must be an integer greater than zero or None.')
            try :
                originalStackSize = _thread.stack_size(workersStackSize)
            except :
                raise MicroWorkersException('"workersStackSize" of %s cannot be used.' % workersStackSize)
        try :
            for x in range(workersCount) :
                _thread.start_new_thread(self._workerThreadFunc, (None, ))
        except Exception as ex :
            raise MicroWorkersException('Error to create workers : %s' % ex)
        if originalStackSize is not None :
            _thread.stack_size(originalStackSize)

    # ============================================================================
    # ===( Functions )============================================================
    # ============================================================================

    def AddJob(self, name, function, arg=None, onFinished=None) :
        if function :
            self._jobs.append( (name, function, arg, onFinished) )
            print('MicroWorkers: Job %s added' % name)
            try :
                self._workersLock.release()
            except :
                pass

    # ============================================================================
    # ===( Properties )===========================================================
    # ============================================================================

    @property
    def Count(self) :
        return self._workersCount

    # ----------------------------------------------------------------------------

    @property
    def JobsInQueue(self) :
        return len(self._jobs)

    # ----------------------------------------------------------------------------

    @property
    def JobsInProcess(self) :
        return self._jobsPrcCount

    # ----------------------------------------------------------------------------

    @property
    def IsWorking(self) :
        return (len(self._jobs) > 0 or self._jobsPrcCount > 0)

    # ============================================================================
    # ============================================================================
    # ============================================================================