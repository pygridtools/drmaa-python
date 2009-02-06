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

"""drmaa errors"""

from ctypes import create_string_buffer
from drmaa.const import ERROR_STRING_BUFFER

class AlreadyActiveSessionException(Exception):
    pass
class AuthorizationException(Exception):
    pass
class ConflictingAttributeValuesException(AttributeError):
    pass
class DefaultContactStringException(Exception):
    pass
class DeniedByDrmException(Exception):
    pass
class DrmCommunicationException(Exception):
    pass
class DrmsExitException(Exception):
    pass
class DrmsInitException(Exception):
    pass
class ExitTimeoutException(Exception):
    pass
class HoldInconsistentStateException(Exception):
    pass
class IllegalStateException(Exception):
    pass
class InternalException(Exception):
    pass
class InvalidAttributeFormatException(AttributeError):
    pass
class InvalidContactStringException(Exception):
    pass
class InvalidJobException(Exception):
    pass
class InvalidJobTemplateException(Exception):
    pass
class NoActiveSessionException(Exception):
    pass
class NoDefaultContactStringSelectedException(Exception):
    pass
class ReleaseInconsistentStateException(Exception):
    pass
class ResumeInconsistentStateException(Exception):
    pass
class SuspendInconsistentStateException(Exception):
    pass
class TryLaterException(Exception):
    pass
class UnsupportedAttributeException(AttributeError):
    pass
class InvalidArgumentException(AttributeError):
    pass
class InvalidAttributeValueException(AttributeError):
    pass
class OutOfMemoryException(MemoryError):
    pass

error_buffer = create_string_buffer(ERROR_STRING_BUFFER)

def error_check(code):
    if code == 0: return 
    else:
        try:
            raise _ERRORS[code-1]("code %s: %s" % (code, error_buffer.value))
        except IndexError:
            raise Exception("code %s: %s" % (code, error_buffer.value))

# da vedere: NO_RUSAGE, NO_MORE_ELEMENTS
_ERRORS = [ InternalException,
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
            StopIteration ]

