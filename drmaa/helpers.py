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
#  Author: Dan Blanchard <dblanchard@ets.org>

"""
internal helpers
"""

from __future__ import absolute_import, print_function, unicode_literals

import sys
from collections import namedtuple
from ctypes import (byref, c_uint, create_string_buffer, POINTER, pointer,
                    sizeof)

from drmaa.const import ATTR_BUFFER, ENCODING, NO_MORE_ELEMENTS
from drmaa.errors import error_buffer
from drmaa.wrappers import (drmaa_attr_names_t, drmaa_attr_values_t,
                            drmaa_get_attribute, drmaa_get_attribute_names,
                            drmaa_get_next_attr_name,
                            drmaa_get_next_attr_value,
                            drmaa_get_next_job_id, drmaa_get_vector_attribute,
                            drmaa_get_vector_attribute_names, drmaa_job_ids_t,
                            drmaa_release_attr_names,
                            drmaa_release_attr_values,
                            drmaa_release_job_ids, drmaa_run_bulk_jobs,
                            drmaa_set_attribute, drmaa_set_vector_attribute,
                            drmaa_version, STRING)


# Python 3 compatability help
if sys.version_info < (3, 0):
    bytes = str
    str = unicode


_BUFLEN = ATTR_BUFFER


class BoolConverter(object):

    """Helper class to convert to/from bool attributes."""

    def __init__(self, true=b'y', false=b'n'):
        if isinstance(true, str):
            true = true.encode(ENCODING)
        self.true = true
        if isinstance(false, str):
            false = false.encode(ENCODING)
        self.false = false

    def to_drmaa(self, value):
        if value:
            return self.true
        else:
            return self.false

    def from_drmaa(self, value):
        if value == self.true:
            return True
        else:
            return False


class IntConverter(object):

    """Helper class to convert to/from int attributes."""
    @staticmethod
    def to_drmaa(value):
        return bytes(value)

    @staticmethod
    def from_drmaa(value):
        return int(value)


class SessionStringAttribute(object):

    def __init__(self, drmaa_function):
        self._f = drmaa_function

    def __get__(self, *args):
        buf = create_string_buffer(_BUFLEN)
        c(self._f, buf, sizeof(buf))
        return buf.value.decode()

Version = namedtuple("Version", "major minor")
if sys.version_info < (3, 0):
    Version.__str__ = lambda x: "{0}.{1}".format(x.major,
                                                 x.minor).encode(ENCODING)
else:
    Version.__str__ = lambda x: "{0}.{1}".format(x.major, x.minor)

class SessionVersionAttribute(object):

    """A Version attribute."""

    def __get__(self, *args):
        major = c_uint(10)
        minor = c_uint(10)
        c(drmaa_version, byref(major), byref(minor))
        return Version(major.value, minor.value)


class Attribute(object):

    """
    A DRMAA attribute, to be managed with scalar C DRMAA attribute management
    functions.
    """

    def __init__(self, name, type_converter=None):
        """
        Attribute constructor.

        :Parameters:
         `name` : string
           name of the attribute to be managed, as seen by the underlying C
           DRMAA
         `type_converter`
           a converter to translate attribute values to/from the underlying
           implementation. See BoolConverter for an example.
        """
        if isinstance(name, str):
            name = name.encode(ENCODING)
        self.name = name
        self.converter = type_converter

    def __set__(self, instance, value):
        if self.converter:
            v = self.converter.to_drmaa(value)
        elif isinstance(value, str):
            v = value.encode(ENCODING)
        else:
            v = value
        c(drmaa_set_attribute, instance, self.name, v)

    def __get__(self, instance, _):
        attr_buffer = create_string_buffer(ATTR_BUFFER)
        c(drmaa_get_attribute, instance, self.name, attr_buffer,
          sizeof(attr_buffer))
        if self.converter:
            return self.converter.from_drmaa(attr_buffer.value)
        elif isinstance(attr_buffer.value, bytes):
            return attr_buffer.value.decode()
        else:
            return attr_buffer.value


class VectorAttribute(object):

    """
    A DRMAA attribute representing a list.

    To be managed with vector C DRMAA attribute management functions.
    """

    def __init__(self, name):
        if isinstance(name, str):
            name = name.encode(ENCODING)
        self.name = name

    def __set__(self, instance, value):
        c(drmaa_set_vector_attribute, instance,
          self.name, string_vector(value))

    def __get__(self, instance, _):
        return list(vector_attribute_iterator(instance, self.name))


class DictAttribute(object):

    """
    A DRMAA attribute representing a python dict.

    To be managed with vector C DRMAA attribute management functions.
    """

    def __init__(self, name):
        if isinstance(name, str):
            name = name.encode(ENCODING)
        self.name = name

    def __set__(self, instance, value):
        vector = []
        for k, v in value.items():
            if isinstance(k, bytes):
                k = k.decode(ENCODING)
            if isinstance(v, bytes):
                v = v.decode(ENCODING)
            vector.append("{0}={1}".format(k, v).encode(ENCODING))
        c(drmaa_set_vector_attribute, instance, self.name,
          string_vector(vector))

    def __get__(self, instance, _):
        x = [i.split('=', 1) for i in
             list(vector_attribute_iterator(instance, self.name))]
        return dict(x)


def attributes_iterator(attributes):
    try:
        buf = create_string_buffer(ATTR_BUFFER)
        while drmaa_get_next_attr_value(attributes, buf,
                                        sizeof(buf)) != NO_MORE_ELEMENTS:
            yield buf.value.decode()
    except:
        drmaa_release_attr_values(attributes)
        raise
    else:
        drmaa_release_attr_values(attributes)


def adapt_rusage(rusage):
    """
    Transform a rusage data structure into a dict.

    Due to the value possibly containing a equal sign make sure we
    limit the splits to only the first occurrence.
    """
    rv = dict()
    for attr in attributes_iterator(rusage.contents):
        
        k, v = attr.split('=',1)
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
        name = create_string_buffer(_BUFLEN)
        while drmaa_get_next_attr_name(attrn_p.contents, name,
                                       _BUFLEN) != NO_MORE_ELEMENTS:
            yield name.value.decode()
    except:
        drmaa_release_attr_names(attrn_p.contents)
        raise
    else:
        drmaa_release_attr_names(attrn_p.contents)


def vector_attribute_names_iterator():
    attrn_p = pointer(POINTER(drmaa_attr_names_t)())
    c(drmaa_get_vector_attribute_names, attrn_p)
    try:
        name = create_string_buffer(_BUFLEN)
        while drmaa_get_next_attr_name(attrn_p.contents, name,
                                       _BUFLEN) != NO_MORE_ELEMENTS:
            yield name.value.decode()
    except:
        drmaa_release_attr_names(attrn_p.contents)
        raise
    else:
        drmaa_release_attr_names(attrn_p.contents)


def run_bulk_job(jt, start, end, incr=1):
    jids = pointer(POINTER(drmaa_job_ids_t)())
    try:
        c(drmaa_run_bulk_jobs, jids, jt, start, end, incr)
        jid = create_string_buffer(_BUFLEN)
        while drmaa_get_next_job_id(jids.contents, jid,
                                    _BUFLEN) != NO_MORE_ELEMENTS:
            yield jid.value.decode()
    except:
        drmaa_release_job_ids(jids.contents)
        raise
    else:
        drmaa_release_job_ids(jids.contents)


def c(f, *args):
    """
    A helper function wrapping calls to the C DRMAA functions with error
    managing code.
    """
    return f(*(args + (error_buffer, sizeof(error_buffer))))


def string_vector(v):
    vlen = len(v)
    values = (STRING * (vlen + 1))()
    for i, el in enumerate(v):
        values[i] = STRING(el.encode(ENCODING) if isinstance(el, str) else el)
    values[vlen] = STRING()
    return values


def attribute_setter(obj, attribute_name):
    """
    returns a drmaa attribute setter
    """
    def f(value):
        "setter for %s" % attribute_name
        c(drmaa_set_attribute, obj, attribute_name, value)
    f.__name__ = 'set_' + attribute_name
    return f


def attribute_getter(obj, attribute_name):
    """
    returns a drmaa attribute setter
    """
    def f():
        "getter for %s" % attribute_name
        attr_buffer = create_string_buffer(1024)
        c(drmaa_get_attribute, obj, attribute_name, attr_buffer,
          sizeof(attr_buffer))
        return attr_buffer.value
    f.__name__ = 'get_' + attribute_name
    return f
