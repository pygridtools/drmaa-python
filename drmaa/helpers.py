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

"""internal helpers"""

import ctypes as _ct
from drmaa.wrappers import *
from drmaa.errors import error_buffer
import drmaa.const as const

try:
    import namedtuple as _nt
except ImportError: # pre 2.6 behaviour
    import nt as _nt

class BoolConverter(object):
    """Helper class to convert to/from bool attributes."""
    @staticmethod
    def to_drmaa(value):
        if value: return 'y'
        else: return 'n'
    @staticmethod
    def from_drmaa(value):
        if value == 'y':
            return True
        else:
            return False

class SessionStringAttribute(object):

    def __init__(self, drmaa_function):
        self._f = drmaa_function
    def __get__(self, *args):
        buf = _ct.create_string_buffer(1024)
        c(self._f, buf, _ct.sizeof(buf))
        return buf.value

Version = _nt.namedtuple("Version", "major minor")
Version.__str__ = lambda x: "%s.%s" % (x.major, x.minor)
#Version.__doc__ = """\
#An object representing the DRMAA version.
#
#major and minor attributes are int. For DRMAA 1.0, major == 1 and minor == 0.
#"""

class SessionVersionAttribute(object):
    """A Version attribute."""
    def __get__(self, *args):
        major = _ct.c_uint(10)
        minor = _ct.c_uint(10)
        c(drmaa_version, _ct.byref(major), _ct.byref(minor))
        return Version(major.value, minor.value)

class Attribute(object):
    """A DRMAA attribute, to managed with scalar C DRMAA attribute management functions."""
    def __init__(self, name, type_converter=None):
        """\
Attribute constructor.

:Parameters:
 `name` : string
   name of the attribute to be managed, as seen by the underlying C DRMAA
 `type_converter`
   a converter to translate attribute values to/from the underlying
   implementation. See BoolConverter for an example.
"""
        self.name = name
        self.converter = type_converter
    def __set__(self, instance, value):
        if self.converter:
            v = self.converter.to_drmaa(value)
        else:
            v = value
        c(drmaa_set_attribute, instance, self.name, v)
    def __get__(self, instance, _):
        attr_buffer = create_string_buffer(const.ATTR_BUFFER)
        c(drmaa_get_attribute, instance, self.name, 
          attr_buffer, sizeof(attr_buffer))
        if self.converter:
            return self.converter.from_drmaa(attr_buffer.value)
        else:
            return attr_buffer.value

class VectorAttribute(object):
    """\
A DRMAA attribute representing a list. 

To be managed with vector C DRMAA attribute management functions."""
    def __init__(self, name):
        self.name = name
    def __set__(self, instance, value):
        c(drmaa_set_vector_attribute, instance, self.name, string_vector(value))
    def __get__(self, instance, _):
        return list(vector_attribute_iterator(
                instance, self.name))

class DictAttribute(object):
    """\
A DRMAA attribute representing a python dict.

To be managed with vector C DRMAA attribute management functions."""
    def __init__(self, name):
        self.name = name
    def __set__(self, instance, value):
        v = [ "%s=%s" % (k, v) for (k, v) in value.iteritems() ]
        c(drmaa_set_vector_attribute, instance, self.name, string_vector(v))
    def __get__(self, instance, _):
        return dict([ i.split('=') for i in list(vector_attribute_iterator(
                        instance, self.name)) ])


def attributes_iterator(attributes):
    try:
        buf = create_string_buffer(const.ATTR_BUFFER)
        while drmaa_get_next_attr_value(attributes, buf, sizeof(buf))\
                != const.NO_MORE_ELEMENTS:
            yield buf.value
    finally:
        drmaa_release_attr_values(attributes)

def adapt_rusage(rusage):
    "transform a rusage data structure into a dict"
    rv = dict()
    for attr in attributes_iterator(rusage.contents):
        k, v = attr.split('=')
        rv[k] = v
    return rv

def vector_attribute_iterator(jt, attr_name):
    avalues = pointer(POINTER(drmaa_attr_values_t)())
    c(drmaa_get_vector_attribute, jt, attr_name, avalues)
    return attributes_iterator(avalues.contents)

def attribute_names_iterator():
    attrn_p = pointer(POINTER(drmaa_attr_names_t)())
    c(drmaa_get_attribute_names, attrn_p)
    try: 
        name = create_string_buffer(128)
        while drmaa_get_next_attr_name(attrn_p.contents, name, 128)\
                != const.NO_MORE_ELEMENTS:
            yield name.value
    finally:
        drmaa_release_attr_names(attrn_p.contents)

def vector_attribute_names_iterator():
    attrn_p = pointer(POINTER(drmaa_attr_names_t)())
    c(drmaa_get_vector_attribute_names, attrn_p)
    try:
        name = create_string_buffer(128)
        while drmaa_get_next_attr_name(attrn_p.contents, name, 128)\
                != const.NO_MORE_ELEMENTS:
            yield name.value
    finally:
        drmaa_release_attr_names(attrn_p.contents)

def run_bulk_job(jt, start, end, incr=1):
    jids = pointer(POINTER(drmaa_job_ids_t)())
    try:
        c(drmaa_run_bulk_jobs, jids, jt, start, end, incr)
        jid = create_string_buffer(128)
        while drmaa_get_next_job_id(jids.contents, jid, 128)\
                != const.NO_MORE_ELEMENTS:
            yield jid.value
    finally:
        drmaa_release_job_ids(jids.contents)

def c(f, *args):
    """An helper function wrapping calls to the C DRMAA functions with error managing code."""
    return f(*(args + (error_buffer, sizeof(error_buffer))))

def string_vector(v):
    vlen = len(v)
    values = (STRING * (vlen + 1))()
    for i, el in enumerate(v):
        values[i] = STRING(el)
    values[vlen] = STRING()
    return values

def attribute_setter(obj, attribute_name):
    "returns a drmaa attribute setter"
    def f(value):
        "setter for %s" % attribute_name
        c(drmaa_set_attribute, obj, attribute_name, value)
    f.__name__ = 'set_'+attribute_name
    return f

def attribute_getter(obj, attribute_name):
    "returns a drmaa attribute setter"
    def f():
        "getter for %s" % attribute_name
        attr_buffer = create_string_buffer(1024)
        c(drmaa_get_attribute, obj, attribute_name, attr_buffer, sizeof(attr_buffer))
        return attr_buffer.value
    f.__name__ = 'get_'+attribute_name
    return f
