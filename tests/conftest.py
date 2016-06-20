import pytest
import logging

from tests.utils import TestHandler, TestSocket
from pysllo.formatters.json_formatter import JsonFormatter
from pysllo.handlers import ElasticSearchUDPHandler


@pytest.fixture()
def handler():
    return TestHandler()


@pytest.fixture()
def socket():
    return TestSocket()


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


@pytest.fixture()
def es_handler(socket):
    host, port = 'localhost', 9000
    handler = ElasticSearchUDPHandler([(host, port)], limit=1000)
    handler._connection = socket
    formatter = JsonFormatter(limit=1000)
    handler.setFormatter(formatter)
    return handler


@pytest.fixture()
def es_logger(es_handler):
    log = logging.getLogger('test')
    log.setLevel(logging.DEBUG)
    log.addHandler(es_handler)
    return log
