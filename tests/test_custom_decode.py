from .context import schema, VersionConflictionException

import unittest
import json


def encode(jobj):
    return 'JUNK' + json.dumps(jobj)


def decode(jstr):
    return json.loads(jstr[4:])


class CustomDecodeTest(unittest.TestCase):
    def test_only_default_record(self):
        version, Record = schema(decode=decode)

        @version()
        class Recordv0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record('JUNK{"_ver": 0, "value": 1}')

        self.assertEqual(1, rec.value)

    def test_2_records_from_different_db_doesnt_conflict(self):
        version1, Record1 = schema(decode=decode)

        @version1()
        class Record1v0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record1('JUNK{"_ver": 0, "value": 1}')

        self.assertEqual(1, rec.value)

        version2, Record2 = schema(decode=decode)

        @version2()
        class Record2v0(object):
            def __init__(self, jobj):
                self.value = jobj['value']

        rec = Record2('JUNK{"_ver": 0, "value": 2}')

        self.assertEqual(2, rec.value)

    def test_raise_exception_if_a_version_specified_twice(self):
        def wrapper():
            version, Record = schema(decode=decode)

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
        version, Record = schema(decode=decode)

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

        rec = Record('JUNK{"_ver": 0, "old_name": 1}')

        self.assertEqual(1, rec.new_name)
