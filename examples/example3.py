#!/usr/bin/env python

import DRMAA
import os

def main():
    """Submit a job and wait for it to finish.
    Note, need file called sleeper.sh in home directory. An example:
    echo 'Hello World $1'
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

    retval = s.wait(jobid, DRMAA.Session.TIMEOUT_WAIT_FOREVER)
    print 'Job: ' + str(retval.getJobId()) + ' finished with code ' + str(retval.getExitStatus())

    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
