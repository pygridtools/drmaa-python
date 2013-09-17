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
"""

from __future__ import absolute_import, print_function, unicode_literals

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



__docformat__ = "restructuredtext en"
__version__ = "0.7"


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
           'InvalidAttributeValueException', 'OutOfMemoryException']
