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
#  This program is distributed in the hope that it will be   
#  useful, but WITHOUT ANY WARRANTY; without even the        
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR   
#  PURPOSE. See the license for more details.                
# -----------------------------------------------------------
#  
#  Author: Enrico Sirola <enrico.sirola@statpro.com> 

import ctypes as _ct

try:
    import namedtuple as _nt
except ImportError: # pre 2.6 behaviour
    import nt as _nt

import drmaa.const as _c
from drmaa.const import JobState, JobControlAction, JobSubmissionState
import drmaa.wrappers as _w
import drmaa.helpers as _h
from drmaa.errors import (AlreadyActiveSessionException,
                          AuthorizationException,
                          ConflictingAttributeValuesException,
                          DefaultContactStringException,
                          DeniedByDrmException,
                          DrmCommunicationException,
                          DrmsExitException,
                          DrmsInitException,
                          ExitTimeoutException,
                          HoldInconsistentStateException,
                          IllegalStateException,
                          InternalException,
                          InvalidAttributeFormatException,
                          InvalidContactStringException,
                          InvalidJobException,
                          InvalidJobTemplateException,
                          NoActiveSessionException,
                          NoDefaultContactStringSelectedException,
                          ReleaseInconsistentStateException,
                          ResumeInconsistentStateException,
                          SuspendInconsistentStateException,
                          TryLaterException,
                          UnsupportedAttributeException,
                          InvalidArgumentException,
                          InvalidAttributeValueException,
                          OutOfMemoryException,)

Version = _h.Version
JobInfo = _nt.namedtuple("JobInfo", 
                         """jobId hasExited hasSignal terminatedSignal 
                            hasCoreDump wasAborted resourceUsage""")
# FileTransferMode = _nt.namedtuple("FileTransferMode", 
#                                   """transferInputStream transferOutputStream 
#                                      transferErrorStream""")

class JobTemplate(object):

    HOME_DIRECTORY='$drmaa_hd_ph$'
    WORKING_DIRECTORY='$drmaa_wd_ph$'
    PARAMETRIC_INDEX='$drmaa_incr_ph$'
    # contains list of strings

    # this should probably return the JobTemplate attribute names, not the
    # C API drmaa attribute names
    @property
    def attributeNames(self):
        return list(_h.attribute_names_iterator())

    # scalar attributes
    remoteCommand           = _h.Attribute(_c.REMOTE_COMMAND       )
    jobSubmissionState      = _h.Attribute(_c.JS_STATE             )
    workingDirectory        = _h.Attribute(_c.WD                   )
    jobCategory             = _h.Attribute(_c.JOB_CATEGORY         )
    nativeSpecification     = _h.Attribute(_c.NATIVE_SPECIFICATION )
    blockEmail              = _h.Attribute(_c.BLOCK_EMAIL, type_converter=_h.BoolConverter)
    startTime               = _h.Attribute(_c.START_TIME           )
    jobName                 = _h.Attribute(_c.JOB_NAME             )
    inputPath               = _h.Attribute(_c.INPUT_PATH           )
    outputPath              = _h.Attribute(_c.OUTPUT_PATH          )
    errorPath               = _h.Attribute(_c.ERROR_PATH           )
    joinFiles               = _h.Attribute(_c.JOIN_FILES, type_converter=_h.BoolConverter)
    # the following is available on ge6.2 only if enabled via cluster configuration
    transferFiles           = _h.Attribute(_c.TRANSFER_FILES       )
    # the following are apparently not available on ge 6.2
    # it will raise if you try to access these attrs
    deadlineTime            = _h.Attribute(_c.DEADLINE_TIME        )
    # these will also probably need specific converters (should receive float values)
    hardWallclockTimeLimit  = _h.Attribute(_c.WCT_HLIMIT           )
    softWallclockTimeLimit  = _h.Attribute(_c.WCT_SLIMIT           )
    hardRunDurationLimit    = _h.Attribute(_c.DURATION_HLIMIT      )
    softRunDurationLimit    = _h.Attribute(_c.DURATION_SLIMIT      )

    # vector attributes
    email = _h.VectorAttribute(_c.V_EMAIL)
    args  = _h.VectorAttribute(_c.V_ARGV)
    
    # dict attributes
    environment = _h.DictAttribute(_c.V_ENV)

    _as_parameter_ = None

    def __init__(self):
        jt = _ct.pointer(_ct.POINTER(_w.drmaa_job_template_t)())
        _h.c(_w.drmaa_allocate_job_template, jt)
        self._jt = self._as_parameter_ = jt.contents

    def delete(self):
        _h.c(_w.drmaa_delete_job_template, self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.delete()
        return False

class Session(object):
    TIMEOUT_WAIT_FOREVER=-1
    TIMEOUT_NO_WAIT=0
    JOB_IDS_SESSION_ANY='DRMAA_JOB_IDS_SESSION_ANY'
    JOB_IDS_SESSION_ALL='DRMAA_JOB_IDS_SESSION_ALL'

    contact = _h.SessionStringAttribute(_w.drmaa_get_contact)
    drmsInfo = _h.SessionStringAttribute(_w.drmaa_get_DRM_system)
    drmaaImplementation = _h.SessionStringAttribute(_w.drmaa_get_DRMAA_implementation)
    version = _h.SessionVersionAttribute()

    def __init__(self, contactString=''):
        self.initialize(contactString)

    # no return value
    @staticmethod
    def initialize(contactString=''):
        _w.init(contactString)

    # no return value
    @staticmethod
    def exit():
        _w.exit()

    # returns JobTemplate instance
    @staticmethod
    def createJobTemplate():
        return JobTemplate()

    # takes JobTemplate instance, no return value
    @staticmethod
    def deleteJobTemplate(jobTemplate):
        jobTemplate.delete()

    # takes JobTemplate instance, returns string
    @staticmethod
    def runJob(jobTemplate):
        jid = _ct.create_string_buffer(128)
        _h.c(_w.drmaa_run_job, jid, _ct.sizeof(jid), jobTemplate)
        return jid.value

    # takes JobTemplate instance and num values, returns string list
    @staticmethod
    def runBulkJobs(jobTemplate, beginIndex, endIndex, step):
        return list(_h.run_bulk_job(jobTemplate, beginIndex, endIndex, step))

    # takes string and JobControlAction value, no return value
    @staticmethod
    def control(jobName, operation):
        _w.drmaa_control(jobName, _c.string_to_control_action(operation))

    # takes string list, num value and boolean, no return value
    @staticmethod
    def synchronize(jobList, timeout=-1, dispose=False):
        if dispose: d=1
        else: d=0
        _h.c(_w.drmaa_synchronize, _h.string_vector(jobList), timeout, d)

    # takes string and long, returns JobInfo instance
    @staticmethod
    def wait(jobName, timeout=-1):
        stat = _ct.c_int()
        rusage = _ct.pointer(_ct.POINTER(_w.drmaa_attr_values_t)())
        _h.c(_w.drmaa_wait, jobName, None, 0, _ct.byref(stat), 
             timeout, rusage)
        res_usage = _h.adapt_rusage(rusage)
        exited = _ct.c_int()
        _h.c(_w.drmaa_wifexited, _ct.byref(exited), stat)
        aborted = _ct.c_int()
        _h.c(_w.drmaa_wifaborted, _ct.byref(aborted), stat)
        signaled = _ct.c_int()
        _h.c(_w.drmaa_wifsignaled, _ct.byref(signaled), stat)
        coredumped = _ct.c_int()
        _h.c(_w.drmaa_wcoredump, _ct.byref(coredumped), stat)
        exit_status = _ct.c_int()
        _h.c(_w.drmaa_wexitstatus, _ct.byref(exit_status), stat)
        term_signal = _ct.create_string_buffer(_c.SIGNAL_BUFFER)
        _h.c(_w.drmaa_wtermsig, term_signal, _ct.sizeof(term_signal), stat)
        return JobInfo(jobName, bool(exited), bool(signaled), term_signal.value, 
                       bool(coredumped), bool(aborted), res_usage)

    # takes string, returns JobState instance
    @staticmethod
    def jobStatus(jobName):
        status = _ct.c_int()
        _h.c(_w.drmaa_job_ps, jobName, _ct.byref(status))
        return _c.status_to_string(status.value)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.exit()
        return False
