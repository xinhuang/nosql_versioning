****
NoSQL Versioning
****

A Python library for NoSQL record versioning.

Installation
============

To install the latest release on `PyPi <https://pypi.python.org/pypi/nosql_versioning/0.1>`_,
simply run:

::

  pip install nosql_versioning

Or to install the latest development version, run:

::

  git clone https://github.com/xinhuang/nosql_versioning.git
  cd nosql_versioning
  python setup.py install

Quick Tutorial
==============

.. code:: pycon

  >>> from nosql_versioning import database
  >>>
  >>> version, Record = database()
  >>>
  >>> @version()
  >>> class Recordv0(object):
  >>>     def __init__(self, jobj):
  >>>         self.old_name = jobj['old_name']
  >>>
  >>> @version(1)
  >>> class Recordv1(object):
  >>>     def __init__(self, jobj):
  >>>         self.new_name = jobj['new_name']
  >>>
  >>>     @staticmethod
  >>>     def migrate(jobj):
  >>>         jobj['new_name'] = jobj['old_name']
  >>>         del jobj['old_name']
  >>>
  >>> rec = Record('{"_ver": 0, "old_name": 1}')
  >>> print(rec.new_name)


Licensing
=========

This project is released under the terms of the MIT Open Source License. View
*LICENSE.txt* for more information.
