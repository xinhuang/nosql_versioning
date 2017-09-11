__version__ = '0.1.7'


class VersionConflictionException(Exception):
    def __init__(self, n):
        super().__init__('Version {} has already been specified'.format(n))


def database(version=None, decode=None):
    if version is None:
        def version(o): return o.get('_ver')

    if decode is None:
        def decode(o): return o

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

        def record(*args, **kwargs):
            data = None
            if len(args) == 1 and len(kwargs) == 0:
                data = args[0]
            elif len(args) == 0 and len(kwargs) == 1:
                data = kwargs.get('data')
            if data:
                obj = decode(data)
                n = version(obj)
                if n is None:
                    versions[0].migrate(obj)
                    n = 0
                while n < latest:
                    cls = versions[n + 1]
                    cls.migrate(obj)
                    n += 1
                return versions[latest](obj)
            else:
                return versions[latest](*args, **kwargs)

        return version_descriptor, record

    return instance()
