#!/usr/bin/env python

import DRMAA
import time
import os

def main():
    """Submit a job, and check its progress.
    Note, need file called sleeper.sh in home directory. An example:
    echo 'Hello World $1'
    sleep 30s
    """
    s=DRMAA.Session()
    s.init()

    print 'Creating job template'
    jt = s.createJobTemplate()
    jt.remoteCommand = os.getcwd() + '/sleeper.sh'
    jt.args = ['42','Simon says:']
    jt.joinFiles=True
    jt.outputPath=":"+DRMAA.JobTemplate.HOME_DIRECTORY+'/tmp/DRMAA_JOB_OUT'
    
    jobid = s.runJob(jt)
    print 'Your job has been submitted with id ' + jobid

    # Who needs a case statement when you have dictionaries?
    decodestatus = {
        DRMAA.Session.UNDETERMINED: 'process status cannot be determined',
        DRMAA.Session.QUEUED_ACTIVE: 'job is queued and active',
        DRMAA.Session.SYSTEM_ON_HOLD: 'job is queued and in system hold',
        DRMAA.Session.USER_ON_HOLD: 'job is queued and in user hold',
        DRMAA.Session.USER_SYSTEM_ON_HOLD: 'job is queued and in user and system hold',
        DRMAA.Session.RUNNING: 'job is running',
        DRMAA.Session.SYSTEM_SUSPENDED: 'job is system suspended',
        DRMAA.Session.USER_SUSPENDED: 'job is user suspended',
        DRMAA.Session.DONE: 'job finished normally',
        DRMAA.Session.FAILED: 'job finished, but failed',
        }

    for ix in range(10):
        print 'Checking ' + str(ix) + ' of 10 times'
        status = s.getJobProgramStatus(jobid)
        print decodestatus.get(status)
        time.sleep(5)
    
    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
