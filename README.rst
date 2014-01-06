DRMAA Python
------------

.. image:: https://travis-ci.org/drmaa-python/drmaa-python.png
   :target: https://travis-ci.org/drmaa-python/drmaa-python
   :alt: Travis build status

.. image:: https://coveralls.io/repos/drmaa-python/drmaa-python/badge.png
  :target: https://coveralls.io/r/drmaa-python/drmaa-python
  :alt: Test coverage

.. image:: https://pypip.in/d/drmaa/badge.png
   :target: https://crate.io/packages/drmaa
   :alt: PyPI downloads

.. image:: https://pypip.in/v/drmaa/badge.png
   :target: https://crate.io/packages/drmaa
   :alt: Latest version on PyPI

.. image:: https://d2weczhvl823v0.cloudfront.net/drmaa-python/drmaa-python/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

`Distributed Resource Management Application API <http://en.wikipedia.org/wiki/DRMAA>`__
(DRMAA) bindings for Python. For more information
`read the docs <http://drmaa-python.readthedocs.org>`__.

Requirements
~~~~~~~~~~~~

-  Python 2.6+
-  A DRMAA-compatible cluster (e.g., Grid Engine)

License
~~~~~~~

-  BSD (3 Clause)

Changelog
~~~~~~~~~

-  v0.7.4
   
   -  Switch to using preferred encoding from ``locale`` module for converting 
      strings to binary. This should prevent some lingering ``UnicodeEncodeError`` 
      crashes on Python 2.7.

-  v0.7.3
   
   -  Fix a couple crashes when certain functions that expect ``str`` were passed 
      integers.

-  v0.7.2
   
   -  Fix a couple inconsistencies with ``str`` vs ``bytes`` in Python 3 in 
      ``drmaa.session``.

-  v0.7.1

   -  Add `Read The Docs documentation <http://drmaa-python.readthedocs.org>`__
   -  Add ``const`` module identifiers back into package namespace
   -  Remove ``b`` prefixes from strings inserted into error messages.

-  v0.7.0

   -  String attribute issues with Python 3 have all been resolved, and now each
      function that takes a string can handle unicode strings, and returns
      unicode strings.
   -  All code has been updated to use future imports for ``unicode_literals``
      and ``print_function``, so we're effectively writing Python 3 code now.
   -  PEP8 compliance changes all over the place, except those that would break
      names required by underlying C DRMAA library.
   -  Now automatically run unit tests of Travis-CI with SGE, and all tests pass
      for Python 2.6, 2.7, and 3.3.  SGE is installed using scripts I describe
      in `this gist <https://gist.github.com/dan-blanchard/6586533>`__.
   -  Unit tests are now in a top-level directory instead of a sub-directory
      under the drmaa package.
   -  There is now a `session.py` module that contains most of the code that was
      in ``__init__.py`` before, and ``__init__`` just imports things and sets
      ``__all__`` and ``__version__``, as is typically recommended now.
   -  Drops support for Python 2.5.
