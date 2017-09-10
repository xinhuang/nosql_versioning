import json

__version__ = '0.1.1'


class VersionConflictionException(Exception):
    def __init__(self, n):
        super().__init__('Version {} has already been specified'.format(n))


def database():
    def instance():
        versions = {}
        latest = -1

        def version(n=0):
            def wrapper(cls):
                if n in versions:
                    raise VersionConflictionException(n)
                versions[n] = cls
                nonlocal latest
                latest = max(latest, n)
                return cls
            return wrapper

        def record(jstr):
            jobj = json.loads(jstr)
            n = jobj['_ver']
            while n < latest:
                cls = versions[n + 1]
                cls.migrate(jobj)
                n += 1
            jobj['_ver'] = latest
            return versions[latest](jobj)

        return version, record

    return instance()
