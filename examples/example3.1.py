#!/usr/bin/env python

import drmaa
import os

def main():
    """Submit an array job, and wait for all of them to finish.
    Note, need file called sleeper.sh in home directory.
    """
    s = drmaa.Session()
    s.initialize()
    print 'Creating job template'
    jt = s.createJobTemplate()
    jt.remoteCommand = os.getcwd() + '/sleeper.sh'
    jt.args = ['42','Simon says:']
    jt.joinFiles=True
    
    joblist = s.runBulkJobs(jt,1,30,2)
    print 'Your job has been submitted with id ' + str(joblist)

    s.synchronize(joblist, drmaa.Session.TIMEOUT_WAIT_FOREVER, True)

    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
