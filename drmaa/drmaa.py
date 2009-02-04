# -----------------------------------------------------------
#  Copyright (C) 2008 StatPro Italia s.r.l. 
#                                                            
#  StatPro Italia                                            
#  Via G. B. Vico 4                                          
#  I-20123 Milano                                            
#  ITALY                                                     
#                                                            
#  phone: +39 02 96875 1                                     
#  fax:   +39 02 96875 605                                   
#                                                            
#  email: info@riskmap.net                                   
#                                                            
#  This program is distributed in the hope that it will be   
#  useful, but WITHOUT ANY WARRANTY; without even the        
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR   
#  PURPOSE. See the license for more details.                
# -----------------------------------------------------------
#  
#  Author: Enrico Sirola <enrico.sirola@statpro.com> 
#  $Id$ 

"""This is drmaa.py, implementing the DRMAA Python language binding
Visit www.drmaa.org for details"""

from const import *
from errors import *

class FileTransferMode(object): 
    transferInputStream=False
    transferOutputStream=False
    transferErrorStream=False
    def __cmp__(self,other):
        pass

class Version(object):
    major='1'
    minor='0'
    def __cmp__(self,other):
        pass
    def __str__(self):
        return self.major+'.'+self.minor

class JobInfo(object):
    def __init__(self):
        self.resourceUsage={}
        self.jobId=''
        self.hasExited=False
        self.exitStatus=0
        self.hasSignaled=False
        self.terminatingSignal=''
        self.hasCoreDump=False
        self.wasAborted=False

class JobTemplate(object):
    HOME_DIRECTORY='$drmaa_hd_ph$'
    WORKING_DIRECTORY='$drmaa_wd_ph$'
    PARAMETRIC_INDEX='$drmaa_incr_ph$'
    # contains list of strings
    attributeNames=[]
    def __init__(self):
        self.remoteCommand=''
        self.jobEnvironment={}		
        self.workingDirectory=''
        self.jobCategory=''
        self.nativeSpecification=''
        self.blockEmail=False
        self.jobName=''
        self.inputPath=''
        self.outputPath=''
        self.errorPath=''
        self.joinFiles=False
        # contains list of strings
        self.args=[]				
        # contains one of the job submission state values, or None
        self.jobSubmissionState=None   
        # contains list of strings
        self.email=[]			
        # [[[[CC]YY/]MM/]DD]hh:mm[:ss] [{-|+}UU:uu]
        self.startTime=''			 
        self.deadlineTime=''
        # contains FileTransferMode instance, or None 
        self.transferFiles=None
        # in seconds
        self.hardWallclockTimeLimit=0
        self.softWallClockTimeLimit=0
        self.hardRunDurationLimit=0
        self.softRunDurationLimit=0

class Session(object):
    TIMEOUT_WAIT_FOREVER=-1
    TIMEOUT_NO_WAIT=0
    JOB_IDS_SESSION_ANY='DRMAA_JOB_IDS_SESSION_ANY'
    JOB_IDS_SESSION_ALL='DRMAA_JOB_IDS_SESSION_ALL'
    version=Version()
    contact=''
    drmsInfo=''
    drmaaImplementation=''

    # no return value
    def initialize(self, contactString=''):
        pass
    # no return value
    def exit(self):
        pass
    # returns JobTemplate instance
    def createJobTemplate(self):
        pass
    # takes JobTemplate instance, no return value
    def deleteJobTemplate(self, jobTemplate):
        pass
    # takes JobTemplate instance, returns string
    def runJob(self, jobTemplate):
        pass
    # takes JobTemplate instance and num values, returns string list
    def runBulkJobs(self, jobTemplate, beginIndex, endIndex, step):
        pass
    # takes string and JobControlAction value, no return value
    def control(self, jobName, operation):
        pass
    # takes string list, num value and boolean, no return value
    def synchronize(self, jobList, timeout, dispose):
        pass
    # takes string and long, returns JobInfo instance
    def wait(self, jobName, timeout):
        pass
    # takes string, returns JobState instance
    def jobStatus(jobName):
        pass


