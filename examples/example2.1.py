#!/usr/bin/env python

import drmaa
import os

def main():
    """Submit an array job.
    Note, need file called sleeper.sh in home directory.
    """
    s = drmaa.Session()
    s.initialize()
    print 'Creating job template'
    jt = s.createJobTemplate()
    jt.remoteCommand = os.getcwd() + '/sleeper.sh'
    jt.args = ['42','Simon says:']
    jt.joinFiles=True

    jobid = s.runBulkJobs(jt,1,30,2)
    print 'Your job has been submitted with id ' + str(jobid)

    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
