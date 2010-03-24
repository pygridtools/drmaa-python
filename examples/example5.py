#!/usr/bin/env python

import drmaa
import time
import os

def main():
    """Submit a job, and check its progress.
    Note, need file called sleeper.sh in home directory.
    """
    s = drmaa.Session()
    s.initialize()
    print 'Creating job template'
    jt = s.createJobTemplate()
    jt.remoteCommand = os.getcwd() + '/sleeper.sh'
    jt.args = ['42','Simon says:']
    jt.joinFiles=True
    
    jobid = s.runJob(jt)
    print 'Your job has been submitted with id ' + jobid

    # Who needs a case statement when you have dictionaries?
    decodestatus = {
        drmaa.JobState.UNDETERMINED: 'process status cannot be determined',
        drmaa.JobState.QUEUED_ACTIVE: 'job is queued and active',
        drmaa.JobState.SYSTEM_ON_HOLD: 'job is queued and in system hold',
        drmaa.JobState.USER_ON_HOLD: 'job is queued and in user hold',
        drmaa.JobState.USER_SYSTEM_ON_HOLD: 'job is queued and in user and system hold',
        drmaa.JobState.RUNNING: 'job is running',
        drmaa.JobState.SYSTEM_SUSPENDED: 'job is system suspended',
        drmaa.JobState.USER_SUSPENDED: 'job is user suspended',
        drmaa.JobState.DONE: 'job finished normally',
        drmaa.JobState.FAILED: 'job finished, but failed',
        }

    for ix in range(10):
        print 'Checking ' + str(ix) + ' of 10 times'
        print decodestatus[s.jobStatus(jobid)]
        time.sleep(5)
    
    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
