from .context import database, VersionConflictionException

import unittest


class CustomKeyTest(unittest.TestCase):
    def test_only_default_record(self):
        version, Record = database(version=lambda o: o['__ver'])

        @version()
        class Recordv0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record('{"__ver": 0, "value": 1}')

        self.assertEqual(1, rec.value)

    def test_2_records_from_different_db_doesnt_conflict(self):
        version1, Record1 = database(version=lambda o: o['__ver'])

        @version1()
        class Record1v0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record1('{"__ver": 0, "value": 1}')

        self.assertEqual(1, rec.value)

        version2, Record2 = database(version=lambda o: o['__ver'])

        @version2()
        class Record2v0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record2('{"__ver": 0, "value": 2}')

        self.assertEqual(2, rec.value)

    def test_raise_exception_if_a_version_specified_twice(self):
        def wrapper():
            version, Record = database(version=lambda o: o['__ver'])

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
        version, Record = database(version=lambda o: o['__ver'])

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

        rec = Record('{"__ver": 0, "old_name": 1}')

        self.assertEqual(1, rec.new_name)

    def test_if_no_version_specified(self):
        version, Record = database(
            version=lambda o: o['__ver'] if '__ver' in o else None)

        @version()
        class Recordv0(object):
            def __init__(self, data):
                self.value = data['value']

            @staticmethod
            def migrate(data):
                data['__ver'] = 0
                data['value'] = 42

        rec = Record('{"value": 1}')

        self.assertEqual(42, rec.value)
