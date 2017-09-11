****************
NoSQL Versioning
****************

A Python library for NoSQL record versioning.

Installation
============

To install the latest release on `PyPi <https://pypi.python.org/pypi/nosql_versioning>`_,
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
  >>> import json
  >>>
  >>> version, Record = database(decode=json.loads)
  >>>
  >>> @version()
  >>> class Recordv0(object):
  >>>     def __init__(self, data):
  >>>         self.old_name = data['old_name']
  >>>
  >>> @version(1)
  >>> class Recordv1(object):
  >>>     def __init__(self, data=None, value=None):
  >>>         if data:
  >>>             self.new_name = data['new_name']
  >>>         else:
  >>>             self.new_name = value
  >>>
  >>>     @staticmethod
  >>>     def migrate(data):
  >>>         data['new_name'] = data['old_name']
  >>>         del data['old_name']
  >>>
  >>> rec = Record('{"_ver": 0, "old_name": 1}')
  >>> print(rec.new_name)
  1
  >>> rec = Record(value=42)         # custom constructor can also be used
  >>> print(rec.new_name)
  42


API Reference
=============

``database(decode=None, version=None)``

  :Args:
    * ``decode``: Optional function to deserialize objects retrieved from database.
    * ``version``: Get version from record. By default it's ``data.get('_ver')``

Licensing
=========

This project is released under the terms of the MIT Open Source License. View
*LICENSE.txt* for more information.
