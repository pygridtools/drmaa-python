#!/usr/bin/env python

import DRMAA
import os

def main():
    """Submit an array job.
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

    jobid = s.runBulkJobs(jt,1,30,2)
    print 'Your job has been submitted with id ' + str(jobid)

    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
