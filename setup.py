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

from setuptools import setup, find_packages

packages = find_packages()
package_data = dict([ (x, ['test/*.py']) for x in packages])

setup(
    name="drmaa",
    version="0.4a2",
    packages=packages,
    package_data=package_data,
    author="Enrico Sirola",
    author_email="enrico.sirola@gmail.com",
    description="a python DRMAA library",
    license="BSD",
    keywords="python grid hpc drmaa",
    url="http://drmaa-python.googlecode.com",
    download_url="http://code.google.com/p/drmaa-python/downloads/list",
    tests_require='nose',
    test_suite='nose.collector',
    classifiers="""\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Operating System :: OS Independent
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Programming Language :: Python :: 2
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Distributed Computing""".split('\n'),
)
    

