#!/bin/python
import drmaa
import os
from sys import argv, exit
from time import sleep
from pprint import pprint

NBULKS = 1
JOB_CHUNK = 3

OPATH=":"+drmaa.JobTemplate.HOME_DIRECTORY+'/DRMAA_JOB_OUT'

def init_job_template(jt, path, args, as_bulk_job):
    jt.workingDirectory = drmaa.JobTemplate.HOME_DIRECTORY
    jt.environment = {'a': 'b', 'c':'d',}
    jt.remoteCommand = path
    jt.args = args
    jt.joinFiles=True
    #jt.startTime=datetime.now()
    #print "start time is: ", jt.startTime
    if as_bulk_job:
        jt.outputPath=OPATH+'.'+drmaa.JobTemplate.PARAMETRIC_INDEX
    else:
        jt.outputPath=OPATH
    return jt


def main():
    if len(argv) < 2:
        print "usage: example.py <path-to-job> <arguments>"
        exit(1)
    job_path=argv[1]
    s=drmaa.Session()
    s.initialize()
    # submit some bulk jobs
    jt=init_job_template(s.createJobTemplate(), job_path, argv[2:], True)
    all_jobids = []
    for i in range(NBULKS):
        all_jobids += s.runBulkJobs(jt, 1, JOB_CHUNK, 1)
        sleep(1)
    print "submitted bulk jobs with jobids:"
    pprint(all_jobids)
    # submit some sequential jobs
    s.deleteJobTemplate(jt)
    del jt
    jt=init_job_template(s.createJobTemplate(), job_path, argv[2:], False)
    for i in range(NBULKS):
        all_jobids.append(s.runJob(jt))
        sleep(1)
    s.synchronize(all_jobids,
                  drmaa.Session.TIMEOUT_WAIT_FOREVER,
                  False)
    print "synchronized with all jobs"
    for jid in all_jobids:
        print '-' * 76
        info=s.wait(jid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
        print """\
id:                        %(jobId)s
exited:                    %(hasExited)s
signaled:                  %(hasSignal)s
with signal (id signaled): %(terminatedSignal)s
dumped core:               %(hasCoreDump)s
aborted:                   %(wasAborted)s
resource usage:

%(resourceUsage)s
""" % info._asdict()

if __name__=='__main__':
    main()
