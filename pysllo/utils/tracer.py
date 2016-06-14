import functools


class TraceContext(object):

    def __init__(self, logger):
        self._logger = logger

    def __enter__(self):
        self._logger.enable_tracking()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._logger.exit_with_exc()
            return
        self._logger.disable_tracking()

    def __call__(self, f):
        @functools.wraps(f)
        def decor(*args, **kwargs):
            try:
                self._logger.enable_tracking()
                result = f(*args, **kwargs)
                self._logger.disable_tracking()
                return result
            except Exception:
                self._logger.exit_with_exc()
                raise
        return decor


class Tracer(object):

    def __init__(self):
        self._logs = []

    def log(self, level, msg, args=(), **kwargs):
        self._logs.append((level, msg, args, kwargs))

    def dump_logs(self):
        result = tuple(self._logs)
        self._logs = []
        return result
