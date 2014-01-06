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

"""DRMAA C library function wrappers"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from ctypes import (c_char_p, c_int, c_long, c_size_t, c_uint, c_ulong, CDLL,
                    POINTER, RTLD_GLOBAL, sizeof, Structure)
from ctypes.util import find_library

from drmaa.const import ENCODING
from drmaa.errors import error_check, error_buffer


# Python 3 compatability help
if sys.version_info < (3, 0):
    bytes = str
    str = unicode


# the name of the OS environment variable optionally
# containing the full path to the drmaa library
_drmaa_lib_env_name = 'DRMAA_LIBRARY_PATH'

if _drmaa_lib_env_name in os.environ:
    libpath = os.environ[_drmaa_lib_env_name]
else:
    libpath = find_library('drmaa')

if libpath is None:
    raise RuntimeError(('Could not find drmaa library.  Please specify its ' +
                        'full path using the environment variable ' +
                        '{0}').format(_drmaa_lib_env_name))

_lib = CDLL(libpath, mode=RTLD_GLOBAL)

STRING = c_char_p
size_t = c_ulong
ptrdiff_t = c_int

drmaa_init = _lib.drmaa_init
drmaa_init.restype = error_check
drmaa_init.argtypes = [STRING, STRING, size_t]
drmaa_exit = _lib.drmaa_exit
drmaa_exit.restype = error_check
drmaa_exit.argtypes = [STRING, size_t]


def py_drmaa_init(contact=None):
    if isinstance(contact, str):
        contact = contact.encode(ENCODING)
    return _lib.drmaa_init(contact, error_buffer, sizeof(error_buffer))

_lib.drmaa_exit.argtypes = [c_char_p, c_size_t]
_lib.drmaa_init.restype = error_check


def py_drmaa_exit():
    return _lib.drmaa_exit(error_buffer, sizeof(error_buffer))


# structures
class drmaa_job_template_s(Structure):
    pass
drmaa_job_template_t = drmaa_job_template_s
drmaa_job_template_s._fields_ = []


class drmaa_attr_names_s(Structure):
    pass
drmaa_attr_names_t = drmaa_attr_names_s
drmaa_attr_names_s._fields_ = []


class drmaa_attr_values_s(Structure):
    pass
drmaa_attr_values_t = drmaa_attr_values_s
drmaa_attr_values_s._fields_ = []


class drmaa_job_ids_s(Structure):
    pass
drmaa_job_ids_t = drmaa_job_ids_s
drmaa_job_ids_s._fields_ = []

drmaa_get_contact = _lib.drmaa_get_contact
drmaa_get_contact.restype = error_check
drmaa_get_contact.argtypes = [STRING, size_t, STRING, size_t]
drmaa_version = _lib.drmaa_version
drmaa_version.restype = error_check
drmaa_version.argtypes = [POINTER(c_uint), POINTER(c_uint), STRING, size_t]
drmaa_get_DRM_system = _lib.drmaa_get_DRM_system
drmaa_get_DRM_system.restype = error_check
drmaa_get_DRM_system.argtypes = [STRING, size_t, STRING, size_t]
drmaa_get_DRMAA_implementation = _lib.drmaa_get_DRMAA_implementation
drmaa_get_DRMAA_implementation.restype = error_check
drmaa_get_DRMAA_implementation.argtypes = [STRING, size_t, STRING, size_t]

drmaa_allocate_job_template = _lib.drmaa_allocate_job_template
drmaa_allocate_job_template.restype = error_check
drmaa_allocate_job_template.argtypes = [POINTER(POINTER(drmaa_job_template_t)),
                                        STRING, size_t]
drmaa_delete_job_template = _lib.drmaa_delete_job_template
drmaa_delete_job_template.restype = error_check
drmaa_delete_job_template.argtypes = [POINTER(drmaa_job_template_t), STRING,
                                      size_t]
drmaa_set_attribute = _lib.drmaa_set_attribute
drmaa_set_attribute.restype = error_check
drmaa_set_attribute.argtypes = [POINTER(drmaa_job_template_t), STRING,
                                STRING, STRING, size_t]
drmaa_get_attribute = _lib.drmaa_get_attribute
drmaa_get_attribute.restype = error_check
drmaa_get_attribute.argtypes = [POINTER(drmaa_job_template_t), STRING,
                                STRING, size_t, STRING, size_t]

drmaa_get_next_attr_name = _lib.drmaa_get_next_attr_name
drmaa_get_next_attr_name.restype = c_int
drmaa_get_next_attr_name.argtypes = [POINTER(drmaa_attr_names_t), STRING,
                                     size_t]
drmaa_get_next_attr_value = _lib.drmaa_get_next_attr_value
drmaa_get_next_attr_value.restype = c_int
drmaa_get_next_attr_value.argtypes = [POINTER(drmaa_attr_values_t), STRING,
                                      size_t]
drmaa_get_next_job_id = _lib.drmaa_get_next_job_id
drmaa_get_next_job_id.restype = error_check
drmaa_get_next_job_id.argtypes = [POINTER(drmaa_job_ids_t), STRING, size_t]
drmaa_release_attr_names = _lib.drmaa_release_attr_names
drmaa_release_attr_names.restype = None
drmaa_release_attr_names.argtypes = [POINTER(drmaa_attr_names_t)]
drmaa_release_attr_values = _lib.drmaa_release_attr_values
drmaa_release_attr_values.restype = None
drmaa_release_attr_values.argtypes = [POINTER(drmaa_attr_values_t)]
drmaa_release_job_ids = _lib.drmaa_release_job_ids
drmaa_release_job_ids.restype = None
drmaa_release_job_ids.argtypes = [POINTER(drmaa_job_ids_t)]

drmaa_set_vector_attribute = _lib.drmaa_set_vector_attribute
drmaa_set_vector_attribute.restype = error_check
drmaa_set_vector_attribute.argtypes = [POINTER(drmaa_job_template_t), STRING,
                                       POINTER(STRING), STRING, size_t]
drmaa_get_vector_attribute = _lib.drmaa_get_vector_attribute
drmaa_get_vector_attribute.restype = error_check
drmaa_get_vector_attribute.argtypes = [POINTER(drmaa_job_template_t), STRING,
                                       POINTER(POINTER(drmaa_attr_values_t)),
                                       STRING, size_t]
drmaa_get_attribute_names = _lib.drmaa_get_attribute_names
drmaa_get_attribute_names.restype = error_check
drmaa_get_attribute_names.argtypes = [POINTER(POINTER(drmaa_attr_names_t)),
                                      STRING, size_t]
drmaa_get_vector_attribute_names = _lib.drmaa_get_vector_attribute_names
drmaa_get_vector_attribute_names.restype = error_check
drmaa_get_vector_attribute_names.argtypes = [POINTER(POINTER(drmaa_attr_names_t)),
                                             STRING, size_t]

try:
    drmaa_get_num_attr_names = _lib.drmaa_get_num_attr_names
    drmaa_get_num_attr_names.restype = c_int
    drmaa_get_num_attr_names.argtypes = [POINTER(drmaa_attr_names_t),
                                         POINTER(c_int)]
    drmaa_get_num_attr_values = _lib.drmaa_get_num_attr_values
    drmaa_get_num_attr_values.restype = c_int
    drmaa_get_num_attr_values.argtypes = [POINTER(drmaa_attr_values_t),
                                          POINTER(c_int)]
except AttributeError:  # the above are present from 1.0 onward only
    pass

drmaa_run_job = _lib.drmaa_run_job
drmaa_run_job.restype = error_check
drmaa_run_job.argtypes = [STRING, size_t, POINTER(drmaa_job_template_t), STRING,
                          size_t]
drmaa_run_bulk_jobs = _lib.drmaa_run_bulk_jobs
drmaa_run_bulk_jobs.restype = error_check
drmaa_run_bulk_jobs.argtypes = [POINTER(POINTER(drmaa_job_ids_t)),
                                POINTER(drmaa_job_template_t),
                                c_int, c_int, c_int, STRING, size_t]
drmaa_control = _lib.drmaa_control
drmaa_control.restype = error_check
drmaa_control.argtypes = [STRING, c_int, STRING, size_t]
drmaa_synchronize = _lib.drmaa_synchronize
drmaa_synchronize.restype = error_check
drmaa_synchronize.argtypes = [POINTER(STRING), c_long, c_int, STRING, size_t]
drmaa_wait = _lib.drmaa_wait
drmaa_wait.restype = error_check
drmaa_wait.argtypes = [STRING, STRING, size_t, POINTER(c_int), c_long,
                       POINTER(POINTER(drmaa_attr_values_t)), STRING, size_t]
drmaa_wifexited = _lib.drmaa_wifexited
drmaa_wifexited.restype = error_check
drmaa_wifexited.argtypes = [POINTER(c_int), c_int, STRING, size_t]
drmaa_wexitstatus = _lib.drmaa_wexitstatus
drmaa_wexitstatus.restype = error_check
drmaa_wexitstatus.argtypes = [POINTER(c_int), c_int, STRING, size_t]
drmaa_wifsignaled = _lib.drmaa_wifsignaled
drmaa_wifsignaled.restype = error_check
drmaa_wifsignaled.argtypes = [POINTER(c_int), c_int, STRING, size_t]
drmaa_wtermsig = _lib.drmaa_wtermsig
drmaa_wtermsig.restype = error_check
drmaa_wtermsig.argtypes = [STRING, size_t, c_int, STRING, size_t]
drmaa_wcoredump = _lib.drmaa_wcoredump
drmaa_wcoredump.restype = error_check
drmaa_wcoredump.argtypes = [POINTER(c_int), c_int, STRING, size_t]
drmaa_wifaborted = _lib.drmaa_wifaborted
drmaa_wifaborted.restype = error_check
drmaa_wifaborted.argtypes = [POINTER(c_int), c_int, STRING, size_t]
drmaa_job_ps = _lib.drmaa_job_ps
drmaa_job_ps.restype = error_check
drmaa_job_ps.argtypes = [STRING, POINTER(c_int), STRING, size_t]
drmaa_strerror = _lib.drmaa_strerror
drmaa_strerror.restype = STRING
drmaa_strerror.argtypes = [c_int]
