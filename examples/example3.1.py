#!/usr/bin/env python

import DRMAA
import os

def main():
    """Submit an array job, and wait for all of them to finish
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
    
    joblist = s.runBulkJobs(jt,1,30,2)
    print 'Your job has been submitted with id ' + str(joblist)

    s.synchronize(joblist, DRMAA.Session.TIMEOUT_WAIT_FOREVER, True)

    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
