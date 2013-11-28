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

"""
A python package for DRM job submission and control.

This package is an implementation of the DRMAA 1.0 Python language
binding specification (http://www.ogf.org/documents/GFD.143.pdf).  See
http://drmaa-python.googlecode.com for package info and download.

:author: Enrico Sirola (enrico.sirola@statpro.com)
:author: Dan Blanchard (dblanchard@ets.org)
"""

from __future__ import absolute_import, print_function, unicode_literals

from .const import (ATTR_BUFFER, BLOCK_EMAIL, CONTACT_BUFFER,
                    control_action_to_string, DEADLINE_TIME, DRM_SYSTEM_BUFFER,
                    DRMAA_IMPLEMENTATION_BUFFER, DURATION_HLIMIT,
                    DURATION_SLIMIT, ERROR_PATH, ERROR_STRING_BUFFER,
                    INPUT_PATH, JOB_CATEGORY, JOB_IDS_SESSION_ALL,
                    JOB_IDS_SESSION_ANY, JOB_NAME, job_state, JobControlAction,
                    JOBNAME_BUFFER, JobState, JobSubmissionState, JOIN_FILES,
                    JS_STATE, NATIVE_SPECIFICATION, NO_MORE_ELEMENTS,
                    OUTPUT_PATH, PLACEHOLDER_HD, PLACEHOLDER_INCR,
                    PLACEHOLDER_WD, REMOTE_COMMAND, SIGNAL_BUFFER, START_TIME,
                    status_to_string, string_to_control_action,
                    submission_state, SUBMISSION_STATE_ACTIVE,
                    SUBMISSION_STATE_HOLD, TIMEOUT_NO_WAIT,
                    TIMEOUT_WAIT_FOREVER, TRANSFER_FILES, V_ARGV, V_EMAIL,
                    V_ENV, WCT_HLIMIT, WCT_SLIMIT, WD)
from .errors import (AlreadyActiveSessionException, AuthorizationException,
                     ConflictingAttributeValuesException,
                     DefaultContactStringException, DeniedByDrmException,
                     DrmCommunicationException, DrmsExitException,
                     DrmsInitException, ExitTimeoutException,
                     HoldInconsistentStateException, IllegalStateException,
                     InternalException, InvalidAttributeFormatException,
                     InvalidContactStringException, InvalidJobException,
                     InvalidJobTemplateException, NoActiveSessionException,
                     NoDefaultContactStringSelectedException,
                     ReleaseInconsistentStateException,
                     ResumeInconsistentStateException,
                     SuspendInconsistentStateException, TryLaterException,
                     UnsupportedAttributeException, InvalidArgumentException,
                     InvalidAttributeValueException, OutOfMemoryException)
from .session import JobInfo, JobTemplate, Session
from .version import __version__, VERSION


__docformat__ = "restructuredtext en"


__all__ = ['JobInfo', 'JobTemplate', 'Session', 'AlreadyActiveSessionException',
           'AuthorizationException', 'ConflictingAttributeValuesException',
           'DefaultContactStringException', 'DeniedByDrmException',
           'DrmCommunicationException', 'DrmsExitException',
           'DrmsInitException', 'ExitTimeoutException',
           'HoldInconsistentStateException', 'IllegalStateException',
           'InternalException', 'InvalidAttributeFormatException',
           'InvalidContactStringException', 'InvalidJobException',
           'InvalidJobTemplateException', 'NoActiveSessionException',
           'NoDefaultContactStringSelectedException',
           'ReleaseInconsistentStateException',
           'ResumeInconsistentStateException',
           'SuspendInconsistentStateException', 'TryLaterException',
           'UnsupportedAttributeException', 'InvalidArgumentException',
           'InvalidAttributeValueException', 'OutOfMemoryException',
           'ATTR_BUFFER', 'BLOCK_EMAIL', 'CONTACT_BUFFER',
           'control_action_to_string', 'DEADLINE_TIME', 'DRM_SYSTEM_BUFFER',
           'DRMAA_IMPLEMENTATION_BUFFER', 'DURATION_HLIMIT', 'DURATION_SLIMIT',
           'ERROR_PATH', 'ERROR_STRING_BUFFER', 'INPUT_PATH', 'JOB_CATEGORY',
           'JOB_IDS_SESSION_ALL', 'JOB_IDS_SESSION_ANY', 'JOB_NAME',
           'job_state', 'JobControlAction', 'JOBNAME_BUFFER', 'JobState',
           'JobSubmissionState', 'JOIN_FILES', 'JS_STATE',
           'NATIVE_SPECIFICATION', 'NO_MORE_ELEMENTS', 'OUTPUT_PATH',
           'PLACEHOLDER_HD', 'PLACEHOLDER_INCR', 'PLACEHOLDER_WD',
           'REMOTE_COMMAND', 'SIGNAL_BUFFER', 'START_TIME', 'status_to_string',
           'string_to_control_action', 'submission_state',
           'SUBMISSION_STATE_ACTIVE', 'SUBMISSION_STATE_HOLD',
           'TIMEOUT_NO_WAIT', 'TIMEOUT_WAIT_FOREVER', 'TRANSFER_FILES',
           'V_ARGV', 'V_EMAIL', 'V_ENV', 'WCT_HLIMIT', 'WCT_SLIMIT', 'WD']
