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
#  This program is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE. See the license for more details.
# -----------------------------------------------------------
#
#  Author: Enrico Sirola <enrico.sirola@statpro.com>
#  Author: Dan Blanchard <dblanchard@ets.org>

from setuptools import setup, find_packages

packages = find_packages()
package_data = dict([ (x, ['test/*.py']) for x in packages])

setup(
    name="drmaa",
    version="0.7.1",
    packages=packages,
    package_data=package_data,
    author="David Ressman",
    author_email="davidr@ressman.org",
    description="a python DRMAA library",
    license="BSD",
    keywords="python grid hpc drmaa",
    url="https://github.com/drmaa-python/drmaa-python",
    tests_require='nose',
    test_suite='nose.collector',
    classifiers="""\
Development Status :: 4 - Beta
Operating System :: OS Independent
Intended Audience :: System Administrators
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Distributed Computing""".split('\n'),
)


