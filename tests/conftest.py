import pytest
import logging

from tests.utils import TestHandler


@pytest.fixture()
def handler():
    return TestHandler()


@pytest.fixture(scope='function')
def logger(request, handler):
    def prepare_logger(cls):
        logging.setLoggerClass(cls)
        log = logging.getLogger(cls.__name__.lower())
        assert isinstance(log, cls), \
            'got {!r} from {!r} - expected {!r}'.format(
                log.__class__, log.__module__, cls)
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)
        return log

    def fin():
        logging.setLoggerClass(logging.Logger)
    request.addfinalizer(fin)
    return prepare_logger


@pytest.fixture()
def structured_logger(logger, handler):
    from pysllo.loggers import StructuredLogger
    return logger(StructuredLogger)


@pytest.fixture()
def track_logger(logger, handler):
    from pysllo.loggers import TrackingLogger
    return logger(TrackingLogger)


@pytest.fixture()
def propagation_logger(logger, handler):
    from pysllo.loggers import PropagationLogger
    return logger(PropagationLogger)
