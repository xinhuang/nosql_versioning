__version__ = '0.1.8.2'


class VersionConflictionException(Exception):
    def __init__(self, n):
        super().__init__('Version {} has already been specified'.format(n))


def get_version(data):
    return data.get('_ver')


def decode(o):
    return o


def schema(version=get_version, decode=decode):
    def instance():
        versions = {}
        latest = -1
        staticmethods = {'ver': None, 'methods':[]}

        def update_static_method():
            nonlocal staticmethods
            latest_ver = versions[latest]
            if latest != staticmethods['ver'] and staticmethods['ver']:
                unset_static_method()
            staticmethods['ver'] = latest_ver
            staticmethods['methods'] = []
            for k, v in latest_ver.__dict__.items():
                old = getattr(Record, k) if hasattr(Record, k) else None
                if old is None and isinstance(v, staticmethod):
                    setattr(Record, k, v.__get__(latest_ver))
                    staticmethods['methods'].append(k)

        def unset_static_method():
            nonlocal staticmethods
            for k in staticmethods['methods']:
                delattr(Record, k)

        def version_descriptor(n=0):
            def wrapper(cls):
                if n in versions:
                    raise VersionConflictionException(n)
                versions[n] = cls
                nonlocal latest
                latest = max(latest, n)
                update_static_method()
                return cls
            return wrapper

        def Record(*args, **kwargs):
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

        return version_descriptor, Record

    return instance()
