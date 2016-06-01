import pytest
import logging

from pysllo.loggers.structured_logger import StructuredLogger
from tests.utils import TestHandler


@pytest.fixture()
def handler():
    return TestHandler()


@pytest.fixture()
def logger(handler):
    logging.setLoggerClass(StructuredLogger)
    log = logging.getLogger('test')
    assert isinstance(log, StructuredLogger), \
        'got {!r} from {!r} - expected {!r}'.format(log.__class__, logging, StructuredLogger.__class__)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    return log


def test_simple_debug(logger, handler):
    msg = "TEST"
    logger.debug(msg)
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == logging.getLevelName(logging.DEBUG)
