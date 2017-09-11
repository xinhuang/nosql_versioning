from .context import database, VersionConflictionException

import unittest
import json


class RecordTest(unittest.TestCase):
    def test_only_default_record(self):
        version, Record = database(decode=json.loads)

        @version()
        class Recordv0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record('{"_ver": 0, "value": 1}')

        self.assertEqual(1, rec.value)

    def test_2_records_from_different_db_doesnt_conflict(self):
        version1, Record1 = database(decode=json.loads)

        @version1()
        class Record1v0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record1('{"_ver": 0, "value": 1}')

        self.assertEqual(1, rec.value)

        version2, Record2 = database(decode=json.loads)

        @version2()
        class Record2v0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record2('{"_ver": 0, "value": 2}')

        self.assertEqual(2, rec.value)

    def test_raise_exception_if_a_version_specified_twice(self):
        def wrapper():
            version, Record = database(decode=json.loads)

            @version()
            class Recordv0(object):
                def __init__(self, jobj):
                    self.value = jobj['value']

            @version()
            class Recordv1(object):
                def __init__(self, jobj):
                    self.value = jobj['value']

        self.assertRaises(VersionConflictionException, wrapper)

    def test_record_should_migrate_from_0_to_1(self):
        version, Record = database(decode=json.loads)

        @version()
        class Recordv0(object):
            def __init__(self, jobj):
                self.old_name = jobj['old_name']

        @version(1)
        class Recordv1(object):
            def __init__(self, jobj):
                self.new_name = jobj['new_name']

            @staticmethod
            def migrate(jobj):
                jobj['new_name'] = jobj['old_name']
                del jobj['old_name']

        rec = Record('{"_ver": 0, "old_name": 1}')

        self.assertEqual(1, rec.new_name)

    def test_record_should_instantiate_the_latest_version(self):
        version, Record = database(decode=json.loads)

        @version()
        class Recordv0(object):
            def __init__(self, jobj):
                self.old_name = jobj['old_name']

        @version(1)
        class Recordv1(object):
            def __init__(self, jobj=None, value=None):
                if jobj:
                    self.new_name = jobj['new_name']
                else:
                    self.new_name = value

        rec = Record('{"_ver": 1, "new_name": 1}')

        self.assertEqual(1, rec.new_name)

        rec = Record(value=2)

        self.assertEqual(2, rec.new_name)

    def test_if_no_version_specified(self):
        version, Record = database(decode=json.loads)

        @version()
        class Recordv0(object):
            def __init__(self, data):
                self.value = data['value']

            @staticmethod
            def migrate(data):
                data['_ver'] = 0
                data['value'] = 42

        rec = Record('{"value": 1}')

        self.assertEqual(42, rec.value)
