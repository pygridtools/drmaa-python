DRMAA Python
------------

.. image:: https://travis-ci.org/pygridtools/drmaa-python.svg
   :target: https://travis-ci.org/pygridtools/drmaa-python
   :alt: Travis build status

.. image:: https://coveralls.io/repos/pygridtools/drmaa-python/badge.svg
  :target: https://coveralls.io/r/pygridtools/drmaa-python
  :alt: Test coverage

.. image:: https://pypip.in/d/drmaa/badge.svg
   :target: https://crate.io/packages/drmaa
   :alt: PyPI downloads

.. image:: https://pypip.in/v/drmaa/badge.svg
   :target: https://crate.io/packages/drmaa
   :alt: Latest version on PyPI

`Distributed Resource Management Application API <http://en.wikipedia.org/wiki/DRMAA>`__
(DRMAA) bindings for Python. For more information
`read the docs <http://drmaa-python.readthedocs.org>`__.  

If you simply want to run Python functions on a DRMAA-compatbile grid, use
`GridMap <https://github.com/EducationalTestingService/gridmap>`__.

Requirements
~~~~~~~~~~~~

-  Python 2.6+
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


License
~~~~~~~

-  BSD (3 Clause)

Changelog
~~~~~~~~~

`See GitHub releases <https://github.com/drmaa-python/drmaa-python/releases>`__.
