DRMAA Python
------------

.. image:: https://img.shields.io/travis/pygridtools/drmaa-python/stable.svg
   :alt: Build status
   :target: https://travis-ci.org/pygridtools/drmaa-python

.. image:: https://img.shields.io/coveralls/pygridtools/drmaa-python/stable.svg
    :target: https://coveralls.io/r/pygridtools/drmaa-python

.. image:: https://img.shields.io/pypi/dm/drmaa.svg
   :target: https://warehouse.python.org/project/drmaa/
   :alt: PyPI downloads

.. image:: https://img.shields.io/pypi/v/drmaa.svg
   :target: https://warehouse.python.org/project/drmaa/
   :alt: Latest version on PyPI

.. image:: https://img.shields.io/pypi/l/drmaa.svg
   :alt: License

`Distributed Resource Management Application API <http://en.wikipedia.org/wiki/DRMAA>`__
(DRMAA) bindings for Python. For more information
`read the docs <http://drmaa-python.readthedocs.org>`__.  

If you simply want to run Python functions on a DRMAA-compatible grid, use
`GridMap <https://github.com/pygridtools/gridmap>`__.

Requirements
~~~~~~~~~~~~

-  Python 2.7+
-  A DRMAA-compatible cluster (e.g., Grid Engine)

Installation
~~~~~~~~~~~~

To use the DRMAA Python library, you need to install it via ``pip``:


.. code-block:: bash

   pip install drmaa


and then setup any environment variables that are necessary for your particular DRM system.
For SGE, this means ``SGE_ROOT`` and ``SGE_CELL``, which should be set as follows:


.. code-block:: bash
   
   export SGE_ROOT=/path/to/gridengine
   export SGE_CELL=default


where ``/path/to/gridengine/`` is replaced with the actual path to your Grid Engine installation, 
and ``default`` is replaced with your installation's actual cell. The path is typically 
``/var/lib/gridengine``.

You will also need access to the ``libdrmaa.so.1.0`` C library, which can often be installed as
part of the ``libdrmaa-dev`` package on most Unixes. Once you have installed that, you may need to 
tell DRMAA Python where it is installed by setting the ``DRMAA_LIBRARY_PATH`` environment variable,
if it is not installed in a location that Python usually looks for libraries.


.. code-block:: bash

   export DRMAA_LIBRARY_PATH=/usr/lib/libdrmaa.so.1.0

Acknowledgments
~~~~~~~~~~~~~~~

Thank you to `StatPro <http://www.statpro.com/>`__ and 
`Educational Testing Service <https://github.com/EducationalTestingService>`__ for
funding the development of DRMAA Python.

Changelog
~~~~~~~~~

`See GitHub releases <https://github.com/drmaa-python/drmaa-python/releases>`__.
