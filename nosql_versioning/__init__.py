import json

__version__ = '0.1.2'


class VersionConflictionException(Exception):
    def __init__(self, n):
        super().__init__('Version {} has already been specified'.format(n))


def database(version=None, decode=json.loads):
    if version is None:
        def version(o): return o['_ver']

    def instance():
        versions = {}
        latest = -1

        def version_descriptor(n=0):
            def wrapper(cls):
                if n in versions:
                    raise VersionConflictionException(n)
                versions[n] = cls
                nonlocal latest
                latest = max(latest, n)
                return cls
            return wrapper

        def record(jstr):
            jobj = decode(jstr)
            n = version(jobj)
            while n < latest:
                cls = versions[n + 1]
                cls.migrate(jobj)
                n += 1
            return versions[latest](jobj)

        return version_descriptor, record

    return instance()
