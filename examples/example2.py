#!/usr/bin/env python

import drmaa
import os

def main():
    """Submit a job.
    Note, need file called sleeper.sh in current directory.
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

    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
