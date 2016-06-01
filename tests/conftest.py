import pytest
import logging

from pysllo.loggers.structured_logger import StructuredLogger
from pysllo.loggers.tracking_logger import TrackingLogger
from tests.utils import TestHandler


@pytest.fixture()
def handler():
    return TestHandler()


@pytest.fixture()
def logger(handler):
    def prepare_logger(cls):
        logging.setLoggerClass(cls)
        log = logging.getLogger('test')
        assert isinstance(log, cls), \
            'got {!r} from {!r} - expected {!r}'.format(
                log.__class__, logging, cls.__class__)
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)
        return log
    return prepare_logger


@pytest.fixture()
def struct_logger(logger, handler):
    return logger(StructuredLogger)


@pytest.fixture()
def track_logger(logger, handler):
    return logger(TrackingLogger)
