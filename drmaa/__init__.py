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

"""\
A python package for DRM job submission and control.

This package is an implementation of the DRMAA 1.0 Python language
binding specification (http://www.ogf.org/documents/GFD.143.pdf).  See
http://drmaa-python.googlecode.com for package info and download.
"""

__docformat__ = "restructuredtext en"

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
    """A job to be submitted to the DRM."""

    HOME_DIRECTORY = '$drmaa_hd_ph$'
    """Home directory placeholder."""
    WORKING_DIRECTORY = '$drmaa_wd_ph$'
    """Working directory placeholder."""
    PARAMETRIC_INDEX = '$drmaa_incr_ph$'
    """Parametric index (for job arrays / bulk jobs) placeholder."""

    @property
    def attributeNames(self):
        """\
The list of supported DRMAA scalar attribute names.

This is apparently useless now, and should probably substituted by the
list of attribute names of the JobTemplate instances.
"""
        return list(_h.attribute_names_iterator())

    # scalar attributes
    remoteCommand           = _h.Attribute(_c.REMOTE_COMMAND       )
    """The command to be executed."""
    jobSubmissionState      = _h.Attribute(_c.JS_STATE             )
    """The job status."""
    workingDirectory        = _h.Attribute(_c.WD                   )
    """The job working directory."""
    jobCategory             = _h.Attribute(_c.JOB_CATEGORY         )
    """The job category."""
    nativeSpecification     = _h.Attribute(_c.NATIVE_SPECIFICATION )
    """\
A (DRM-dependant) opaque string to be passed to the DRM representing
other directives.
"""
    blockEmail              = _h.Attribute(_c.BLOCK_EMAIL,
                                           type_converter=_h.BoolConverter)
    """False id this job should send an email, True otherwise."""
    startTime               = _h.Attribute(_c.START_TIME           )
    """The job start time, a partial timestamp string."""
    jobName                 = _h.Attribute(_c.JOB_NAME             )
    """The job Name."""
    inputPath               = _h.Attribute(_c.INPUT_PATH           )
    """The path to a file representing job's stdin."""
    outputPath              = _h.Attribute(_c.OUTPUT_PATH          )
    """The path to a file representing job's stdout."""
    errorPath               = _h.Attribute(_c.ERROR_PATH           )
    """The path to a file representing job's stderr."""
    joinFiles               = _h.Attribute(_c.JOIN_FILES,
                                           type_converter=_h.BoolConverter)
    """True if stdin and stdout should be merged, False otherwise."""
    # the following is available on ge6.2 only if enabled via cluster
    # configuration
    transferFiles           = _h.Attribute(_c.TRANSFER_FILES       )
    """\
True if file transfer should be enabled, False otherwise.

This option might require specific DRM configuration (it does on SGE).
"""
    # the following are apparently not available on ge 6.2
    # it will raise if you try to access these attrs
    deadlineTime            = _h.Attribute(_c.DEADLINE_TIME        )
    """The job deadline time, a partial timestamp string."""
    # these will also probably need specific converters
    # (should receive float values)
    hardWallclockTimeLimit  = _h.Attribute(_c.WCT_HLIMIT           )
    """\
'Hard' Wallclock time limit, in seconds.

The job will be killed by the DRM if it takes more than
'hardWallclockTimeLimit' to complete.
"""
    softWallclockTimeLimit  = _h.Attribute(_c.WCT_SLIMIT           )
    """\
'Soft' Wallclock time limit, in seconds.

The job will be signaled by the DRM if it takes more than
'hardWallclockTimeLimit' to complete.
"""
    hardRunDurationLimit    = _h.Attribute(_c.DURATION_HLIMIT      )
    """\
WRITE ME.
"""
    softRunDurationLimit    = _h.Attribute(_c.DURATION_SLIMIT      )
    """\
WRITE ME.
"""

    # vector attributes
    email = _h.VectorAttribute(_c.V_EMAIL)
    """email addresses to whom send job completion info."""
    args  = _h.VectorAttribute(_c.V_ARGV)
    """The job's command argument list."""
    # dict attributes
    environment = _h.DictAttribute(_c.V_ENV)
    """The job's environment dict."""

    _as_parameter_ = None

    def __init__(self, **kwargs):
        """\
Builds a JobTemplate instance.

Attributes can be passed as keyword arguments."""
        jt = _ct.pointer(_ct.POINTER(_w.drmaa_job_template_t)())
        _h.c(_w.drmaa_allocate_job_template, jt)
        self._jt = self._as_parameter_ = jt.contents
        try:
            for aname in kwargs:
                setattr(self, aname, kwargs.get(aname))
        except:
            self.delete()
            raise

    def delete(self):
        """Deallocate the underlying DRMAA job template."""
        _h.c(_w.drmaa_delete_job_template, self)

    def __enter__(self):
        """context manager enter routine"""
        return self

    def __exit__(self, *_):
        """\
context manager exit routine.

Stops communication with the DRM.
"""
        self.delete()
        return False

class Session(object):
    """\
The DRMAA Session.

This class is the entry point for communicating with the DRM system
"""
    TIMEOUT_WAIT_FOREVER = _c.TIMEOUT_WAIT_FOREVER
    TIMEOUT_NO_WAIT = _c.TIMEOUT_NO_WAIT
    JOB_IDS_SESSION_ANY = _c.JOB_IDS_SESSION_ANY
    JOB_IDS_SESSION_ALL = _c.JOB_IDS_SESSION_ALL

    contact = _h.SessionStringAttribute(_w.drmaa_get_contact)
    """\
a comma delimited string list containing the contact strings available
from the default DRMAA implementation, one element per DRM system
available. If called after initialize(), this method returns the
contact String for the DRM system to which the session is
attached. The returned strings are implementation dependent.
"""

    drmsInfo = _h.SessionStringAttribute(_w.drmaa_get_DRM_system)
    """\
If called before initialize(), this method returns a comma delimited
list of DRM systems, one element per DRM system implementation
provided. If called after initialize(), this method returns the
selected DRM system. The returned String is implementation dependent.
"""
    drmaaImplementation = _h.SessionStringAttribute(
        _w.drmaa_get_DRMAA_implementation)
    """\
If called before initialize(), this method returns a comma delimited
list of DRMAA implementations, one element for each DRMAA
implementation provided. If called after initialize(), this method
returns the selected DRMAA implementation. The returned String is
implementation dependent and may contain the DRM system as a
component.
"""
    version = _h.SessionVersionAttribute()
    """\
a Version object containing the major and minor version numbers of the
DRMAA library. For DRMAA 1.0, major is 1 and minor is 0.
"""
    def __init__(self, contactString=''):
        self.initialize(contactString)

    # no return value
    @staticmethod
    def initialize(contactString=None):
        """\
Used to initialize a DRMAA session for use.

:Parameters:
  contactString : string or None
     implementation-dependent string that
     may be used to specify which DRM system to use

This method must be called before any other DRMAA calls.  If
contactString is None, the default DRM system is used, provided there
is only one DRMAA implementation available. If there is more than one
DRMAA implementation available, initialize() throws a
NoDefaultContactStringSelectedException. initialize() should be called
only once, by only one of the threads. The main thread is
recommended. A call to initialize() by another thread or additional
calls to initialize() by the same thread with throw a
SessionAlreadyActiveException.
"""
        _w.init(contactString)

    # no return value
    @staticmethod
    def exit():
        """\
Used to disengage from DRM.

This routine ends the current DRMAA session but doesn't affect any
jobs (e.g., queued and running jobs remain queued and
running). exit() should be called only once, by only one of the
threads. Additional calls to exit() beyond the first will throw a
NoActiveSessionException.
"""
        _w.exit()

    # returns JobTemplate instance
    @staticmethod
    def createJobTemplate():
        """\
Allocates a new job template.

The job template is used to set the environment for jobs to be
submitted. Once the job template has been created, it should also be
deleted (via deleteJobTemplate()) when no longer needed. Failure to do
so may result in a memory leak.
"""
        return JobTemplate()

    # takes JobTemplate instance, no return value
    @staticmethod
    def deleteJobTemplate(jobTemplate):
        """\
Deallocate a job template.

:Parameters:
  jobTemplate : JobTemplate
    the job temptare to be deleted

This routine has no effect on running jobs.
"""
        jobTemplate.delete()

    # takes JobTemplate instance, returns string
    @staticmethod
    def runJob(jobTemplate):
        """\
Submit a job with attributes defined in the job template.

:Parameters:
  jobTemplate : JobTemplate
    the template representing the job to be run

The returned job identifier is a String identical to that returned
from the underlying DRM system.
"""
        jid = _ct.create_string_buffer(128)
        _h.c(_w.drmaa_run_job, jid, _ct.sizeof(jid), jobTemplate)
        return jid.value

    # takes JobTemplate instance and num values, returns string list
    @staticmethod
    def runBulkJobs(jobTemplate, beginIndex, endIndex, step):
        """\
Submit a set of parametric jobs, each with attributes defined in the job template.

:Parameters:
  jobTemplate : JobTemplate
    the template representng jobs to be run
  beginIndex : int
    index of the first job
  endIndex : int
    index of the last job
  step : int
    the step between job ids

The returned job identifiers are Strings identical to those returned
from the underlying DRM system.  The JobTemplate class defines a
`JobTemplate.PARAMETRIC_INDEX` placeholder for use in specifying paths.
This placeholder is used to represent the individual identifiers of
the tasks submitted through this method.
"""
        return list(_h.run_bulk_job(jobTemplate, beginIndex, endIndex, step))

    # takes string and JobControlAction value, no return value
    @staticmethod
    def control(jobId, operation):
        """\
Used to hold, release, suspend, resume, or kill the job identified by jobId.  

:Parameters:
  jobId : string
    if jobId is `Session.JOB_IDS_SESSION_ALL` then this routine acts on
    all jobs submitted during this DRMAA session up to the moment
    control() is called. The legal values for
    action and their meanings are
  operation : string
    possible values are:
        `JobControlAction.SUSPEND`
          stop the job
        `JobControlAction.RESUME`
          (re)start the job
        `JobControlAction.HOLD`
          put the job on-hold
        `JobControlAction.RELEASE`
          release the hold on the job
        `JobControlAction.TERMINATE`
          kill the job

To avoid thread races in multithreaded applications, the DRMAA
implementation user should explicitly synchronize this call with
any other job submission calls or control calls that may change
the number of remote jobs.

This method returns once the action has been acknowledged by the DRM
system, but does not necessarily wait until the action has been
completed.  Some DRMAA implementations may allow this method to be
used to control jobs submitted external to the DRMAA session, such as
jobs submitted by other DRMAA session in other DRMAA implementations
or jobs submitted via native utilities.
"""
        _h.c(_w.drmaa_control, jobId, _c.string_to_control_action(operation))

    # takes string list, num value and boolean, no return value
    @staticmethod
    def synchronize(jobIds, timeout=-1, dispose=False):
        """\
Waits until all jobs specified by jobList have finished execution.

:Parameters:
  jobIds
    If jobIds contains `Session.JOB_IDS_SESSION_ALL`, then this
    method waits for all jobs submitted during this DRMAA session up to
    the moment synchronize() is called
  timeout : int
    maximum time (in seconds) to be waited for the completion of a job.

    The value `Session.TIMEOUT_WAIT_FOREVER` may be specified to wait
    indefinitely for a result. The value `Session.TIMEOUT_NO_WAIT` may
    be specified to return immediately if no result is available.
  dispose : bool
    specifies how to treat the reaping of the remote job's internal
    data record, which includes a record of the job's consumption of
    system resources during its execution and other statistical
    information. If set to True, the DRM will dispose of the job's
    data record at the end of the synchroniize() call. If set to
    False, the data record will be left for future access via the
    wait() method.

To avoid thread race conditions in multithreaded applications, the
DRMAA implementation user should explicitly synchronize this call with
any other job submission calls or control calls that may change the
number of remote jobs.

If the call exits before the
timeout has elapsed, all the jobs have been waited on or there was an
interrupt. If the invocation exits on timeout, an ExitTimeoutException
is thrown. The caller should check system time before and after this
call in order to be sure of how much time has passed.  
"""
        if dispose: d = 1
        else: d = 0
        _h.c(_w.drmaa_synchronize, _h.string_vector(jobIds), timeout, d)

    # takes string and long, returns JobInfo instance
    @staticmethod
    def wait(jobId, timeout=-1):
        """\
Wait for a job with jobId to finish execution or fail. 

:Parameters:
  `jobId` : str
    The job id to wait completion for.

    If the special string, `Session.JOB_IDS_SESSION_ANY`, is provided as the
    jobId, this routine will wait for any job from the session
  `timeout` : float
    The timeout value is used to specify the desired behavior when a
    result is not immediately available. 

    The value `Session.TIMEOUT_WAIT_FOREVER` may be specified to wait
    indefinitely for a result. The value `Session.TIMEOUT_NO_WAIT` may
    be specified to return immediately if no result is
    available. Alternatively, a number of seconds may be specified to
    indicate how long to wait for a result to become available

This routine is modeled on the wait3 POSIX routine. If the call exits
before timeout, either the job has been waited on successfully or
there was an interrupt. If the invocation exits on timeout, an
`ExitTimeoutException` is thrown. The caller should check system time
before and after this call in order to be sure how much time has
passed.  The routine reaps job data records on a successful call, so
any subsequent calls to wait() will fail, throwing an
`InvalidJobException`, meaning that the job's data record has been
already reaped.  This exception is the same as if the job were
unknown. (The only case where wait() can be successfully called on a
single job more than once is when the previous call to wait() timed
out before the job finished.)
"""
        stat = _ct.c_int()
        rusage = _ct.pointer(_ct.POINTER(_w.drmaa_attr_values_t)())
        _h.c(_w.drmaa_wait, jobId, None, 0, _ct.byref(stat), 
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
        return JobInfo(jobId, bool(exited), bool(signaled),
                       term_signal.value, bool(coredumped),
                       bool(aborted), res_usage)

    # takes string, returns JobState instance
    @staticmethod
    def jobStatus(jobName):
        """\
returns the program status of the job identified by jobId.

The possible values returned from
this method are:

* `JobState.UNDETERMINED`: process status cannot be determined,
* `JobState.QUEUED_ACTIVE`: job is queued and active,
* `JobState.SYSTEM_ON_HOLD`: job is queued and in system hold,
* `JobState.USER_ON_HOLD`: job is queued and in user hold,
* `JobState.USER_SYSTEM_ON_HOLD`: job is queued and in user and system hold,
* `JobState.RUNNING`: job is running,
* `JobState.SYSTEM_SUSPENDED`: job is system suspended,
* `JobState.USER_SUSPENDED`: job is user suspended,
* `JobState.DONE`: job finished normally, and
* `JobState.FAILED`: job finished, but failed.

The DRMAA implementation should always get the status of the job from
the DRM system unless the status has already been determined to be
FAILED or DONE and the status has been successfully cached. Terminated
jobs return a FAILED status.
"""
        status = _ct.c_int()
        _h.c(_w.drmaa_job_ps, jobName, _ct.byref(status))
        return _c.status_to_string(status.value)

    def __enter__(self):
        """Context manager enter function"""
        return self

    def __exit__(self, *_):
        """Context manager exit function."""
        self.exit()
        return False
