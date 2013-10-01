# -----------------------------------------------------------
#  Copyright (C) 2009 StatPro Italia s.r.l.
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

"""
drmaa errors
"""

from ctypes import create_string_buffer

from drmaa.const import ERROR_STRING_BUFFER


class DrmaaException(Exception):

    """
    A common ancestor to all DRMAA Error classes.
    """
    pass


class AlreadyActiveSessionException(DrmaaException):
    pass


class AuthorizationException(DrmaaException):
    pass


class ConflictingAttributeValuesException(DrmaaException, AttributeError):
    pass


class DefaultContactStringException(DrmaaException):
    pass


class DeniedByDrmException(DrmaaException):
    pass


class DrmCommunicationException(DrmaaException):
    pass


class DrmsExitException(DrmaaException):
    pass


class DrmsInitException(DrmaaException):
    pass


class ExitTimeoutException(DrmaaException):
    pass


class HoldInconsistentStateException(DrmaaException):
    pass


class IllegalStateException(DrmaaException):
    pass


class InternalException(DrmaaException):
    pass


class InvalidAttributeFormatException(DrmaaException, AttributeError):
    pass


class InvalidContactStringException(DrmaaException):
    pass


class InvalidJobException(DrmaaException):
    pass


class InvalidJobTemplateException(DrmaaException):
    pass


class NoActiveSessionException(DrmaaException):
    pass


class NoDefaultContactStringSelectedException(DrmaaException):
    pass


class ReleaseInconsistentStateException(DrmaaException):
    pass


class ResumeInconsistentStateException(DrmaaException):
    pass


class SuspendInconsistentStateException(DrmaaException):
    pass


class TryLaterException(DrmaaException):
    pass


class UnsupportedAttributeException(DrmaaException, AttributeError):
    pass


class InvalidArgumentException(DrmaaException, AttributeError):
    pass


class InvalidAttributeValueException(DrmaaException, AttributeError):
    pass


class OutOfMemoryException(DrmaaException, MemoryError):
    pass

error_buffer = create_string_buffer(ERROR_STRING_BUFFER)


def error_check(code):
    if code == 0:
        return
    else:
        error_string = "code {0}: {1}".format(code, error_buffer.value.decode())
        try:
            raise _ERRORS[code - 1](error_string)
        except IndexError:
            raise DrmaaException(error_string)

# da vedere: NO_RUSAGE, NO_MORE_ELEMENTS
_ERRORS = [InternalException,
           DrmCommunicationException,
           AuthorizationException,
           InvalidArgumentException,
           NoActiveSessionException,
           OutOfMemoryException,
           InvalidContactStringException,
           DefaultContactStringException,
           NoDefaultContactStringSelectedException,
           DrmsInitException,
           AlreadyActiveSessionException,
           DrmsExitException,
           InvalidAttributeFormatException,
           InvalidAttributeValueException,
           ConflictingAttributeValuesException,
           TryLaterException,
           DeniedByDrmException,
           InvalidJobException,
           ResumeInconsistentStateException,
           SuspendInconsistentStateException,
           HoldInconsistentStateException,
           ReleaseInconsistentStateException,
           ExitTimeoutException,
           Exception,
           StopIteration]
