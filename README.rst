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

  >>> from nosql_versioning import schema
  >>> import json
  >>>
  >>> version, Record = schema(decode=json.loads)
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
  >>>     @staticmethod
  >>>     def a_staticmethod(n):
  >>>         print(n * 2)
  >>>
  >>> rec = Record('{"_ver": 0, "old_name": 1}')
  >>> print(rec.new_name)
  1
  >>> rec = Record(value=42)         # custom constructor can also be used
  >>> print(rec.new_name)
  42
  >>> Record.a_staticmethod(42)      # static methods defined in the latest version can be used
  84


API Reference
=============

``schema(decode=decode, version=get_version)``
  Create a class descriptor to specify record classes of different version, and a Record initializer to instantiate the latest record from data, or to migrate data to the latest version.

  :Args:
    * ``decode``: Deserialize objects retrieved from database. By default no decoding will be applied.
    * ``version``: Get version from record. By default it's ``data.get('_ver')``

  :Returns:
    * ``version``: A class descriptor to specify record version.
    * ``Record``: A initializer that to construct defined Record class. Migrate if data is not the latest version.

``version(n=0)``
  A class descriptor to specify record class of version N.

  :Args:
    * ``n``: Version. Must be a integer.

  :Raises:
    * ``VersionConflictionException``: When a version is defined twice.

``Record(data=None, *args, **kwargs)``
  The initializer to migrate record to latest and instantiate record class.

  :Args:
    * ``data``: If only this argument is specified, ``decode(data)`` will be used to instantiate the latest record class. (Migrate if needed.)
    * ``args``, ``kwargs``: If not only ``data`` is specified, all arguments will be passed to instantiate the latest record class. No migration.

Migration from Version N-1 to N will use static method ``migrate`` in record class version N.

In case there is no version specified, migration from None to 0 will use static method ``migrate`` in record class Version 0.

Licensing
=========

This project is released under the terms of the MIT Open Source License. View
*LICENSE.txt* for more information.
