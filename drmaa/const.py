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
#  $Id$ 

"""drmaa constants"""

# drmaa_get_attribute()
ATTR_BUFFER = 1024

# drmaa_get_contact() 
CONTACT_BUFFER = 1024

# drmaa_get_DRM_system() 
DRM_SYSTEM_BUFFER = 1024

# drmaa_get_DRM_system() 
DRMAA_IMPLEMENTATION_BUFFER = 1024

# Agreed buffer length constants 
# these are recommended minimum values 

ERROR_STRING_BUFFER =   1024
JOBNAME_BUFFER =        1024
SIGNAL_BUFFER =         32

# Agreed constants 
  
TIMEOUT_WAIT_FOREVER =  -1
TIMEOUT_NO_WAIT =       0 

JOB_IDS_SESSION_ANY =   "DRMAA_JOB_IDS_SESSION_ANY"
JOB_IDS_SESSION_ALL =   "DRMAA_JOB_IDS_SESSION_ALL"

SUBMISSION_STATE_ACTIVE = "drmaa_active"
SUBMISSION_STATE_HOLD =   "drmaa_hold"

# Agreed placeholder names
 
PLACEHOLDER_INCR =       "$drmaa_incr_ph$"
PLACEHOLDER_HD  =        "$drmaa_hd_ph$"
PLACEHOLDER_WD =         "$drmaa_wd_ph$"

# Agreed names of job template attributes 

REMOTE_COMMAND =        "drmaa_remote_command"
JS_STATE =              "drmaa_js_state"
WD =                    "drmaa_wd"
JOB_CATEGORY =          "drmaa_job_category"
NATIVE_SPECIFICATION =  "drmaa_native_specification"
BLOCK_EMAIL =           "drmaa_block_email"
START_TIME =            "drmaa_start_time"
JOB_NAME =              "drmaa_job_name"
INPUT_PATH =            "drmaa_input_path"
OUTPUT_PATH =           "drmaa_output_path"
ERROR_PATH =            "drmaa_error_path"
JOIN_FILES =            "drmaa_join_files"
TRANSFER_FILES =        "drmaa_transfer_files"
DEADLINE_TIME =         "drmaa_deadline_time"
WCT_HLIMIT =            "drmaa_wct_hlimit"
WCT_SLIMIT =            "drmaa_wct_slimit"
DURATION_HLIMIT =       "drmaa_duration_hlimit"
DURATION_SLIMIT =       "drmaa_duration_slimit"

# names of job template vector attributes 
V_ARGV =                "drmaa_v_argv"
V_ENV =                 "drmaa_v_env"
V_EMAIL =               "drmaa_v_email"

NO_MORE_ELEMENTS = 25

def job_state(code):
    return _JOB_PS[code]

class JobState(object):
    UNDETERMINED='undetermined'
    QUEUED_ACTIVE='queued_active'
    SYSTEM_ON_HOLD='system_on_hold'
    USER_ON_HOLD='user_on_hold'
    USER_SYSTEM_ON_HOLD='user_system_on_hold'
    RUNNING='running'
    SYSTEM_SUSPENDED='system_suspended'
    USER_SUSPENDED='user_suspended'
    USER_SYSTEM_SUSPENDED='user_system_suspended'
    DONE='done'
    FAILED='failed'

# Job control action
class JobControlAction(object):
    SUSPEND='suspend'
    RESUME='resume'
    HOLD='hold'
    RELEASE='release'
    TERMINATE='terminate'  

_JOB_CONTROL = [
    JobControlAction.SUSPEND,
    JobControlAction.RESUME,  
    JobControlAction.HOLD,    
    JobControlAction.RELEASE, 
    JobControlAction.TERMINATE
]

def string_to_control_action(operation):
    return _JOB_CONTROL.index(operation)
def control_action_to_string(code):
    return _JOB_CONTROL[code]
def status_to_string(status):
    return _JOB_PS[status]

_JOB_PS = { 
    0x00: JobState.UNDETERMINED,
    0x10: JobState.QUEUED_ACTIVE        ,
    0x11: JobState.SYSTEM_ON_HOLD       ,
    0x12: JobState.USER_ON_HOLD         ,
    0x13: JobState.USER_SYSTEM_ON_HOLD  ,
    0x20: JobState.RUNNING                                   ,
    0x21: JobState.SYSTEM_SUSPENDED     ,
    0x22: JobState.USER_SUSPENDED       ,
    0x23: JobState.USER_SYSTEM_SUSPENDED,
    0x30: JobState.DONE                 ,
    0x40: JobState.FAILED               ,
}                  

# State at submission time
class JobSubmissionState(object):
    HOLD_STATE=SUBMISSION_STATE_HOLD
    ACTIVE_STATE=SUBMISSION_STATE_ACTIVE

_SUBMISSION_STATE = [
    JobSubmissionState.HOLD_STATE,
    JobSubmissionState.ACTIVE_STATE
]

def submission_state(code):
    return _SUBMISSION_STATE[code]
