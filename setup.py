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

# To get around the fact that you can't import stuff from packages in setup.py
exec(compile(open('drmaa/version.py').read(), 'drmaa/version.py', 'exec'))
# (we use the above instead of execfile for Python 3.x compatibility)

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name="drmaa",
      version=__version__,
      packages=packages,
      package_data=package_data,
      author="Dan Blanchard",
      author_email="dblanchard@ets.org",
      description="a python DRMAA library",
      long_description=readme(),
      license="BSD",
      keywords="python grid hpc drmaa",
      url="https://github.com/pygridtools/drmaa-python",
      tests_require='nose',
      test_suite='nose.collector',
      classifiers=["Development Status :: 4 - Beta",
                   "Operating System :: OS Independent",
                   "Intended Audience :: System Administrators",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: BSD License",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 3",
                   "Topic :: Software Development :: Libraries",
                   "Topic :: System :: Distributed Computing"])
