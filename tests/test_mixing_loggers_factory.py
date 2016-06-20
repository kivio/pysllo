import pysllo.loggers as loggers

from pysllo.utils import LoggersFactory
import logging
from logging import Logger

from tests.utils import socket_data


def test_normal_logger():
    MixedLogger = LoggersFactory.make()
    logger = MixedLogger('test')
    assert isinstance(logger, Logger)
    assert not isinstance(logger, loggers.StructuredLogger)
    assert not isinstance(logger, loggers.PropagationLogger)
    assert not isinstance(logger, loggers.TrackingLogger)


def test_structured_logger():
    MixedLogger = LoggersFactory.make(structured_logger=True)
    logger = MixedLogger('test')
    assert isinstance(logger, Logger)
    assert isinstance(logger, loggers.StructuredLogger)
    assert not isinstance(logger, loggers.PropagationLogger)
    assert not isinstance(logger, loggers.TrackingLogger)


def test_propagation_logger():
    MixedLogger = LoggersFactory.make(propagation_logger=True)
    logger = MixedLogger('test')
    assert isinstance(logger, Logger)
    assert not isinstance(logger, loggers.StructuredLogger)
    assert isinstance(logger, loggers.PropagationLogger)
    assert not isinstance(logger, loggers.TrackingLogger)


def test_tracking_logger():
    MixedLogger = LoggersFactory.make(tracking_logger=True)
    logger = MixedLogger('test')
    assert isinstance(logger, Logger)
    assert not isinstance(logger, loggers.StructuredLogger)
    assert isinstance(logger, loggers.PropagationLogger)
    assert isinstance(logger, loggers.TrackingLogger)


def test_mixed_logger():
    MixedLogger = LoggersFactory.make(
        tracking_logger=True,
        propagation_logger=True,
        structured_logger=True
    )
    logger = MixedLogger('test')
    assert isinstance(logger, Logger)
    assert isinstance(logger, loggers.StructuredLogger)
    assert isinstance(logger, loggers.PropagationLogger)
    assert isinstance(logger, loggers.TrackingLogger)


def test_mixed_logger_with_handler(es_handler, socket):
    MixedLogger = LoggersFactory.make(
        tracking_logger=True,
        propagation_logger=True,
        structured_logger=True
    )
    logger = MixedLogger('test')
    logger.addHandler(es_handler)
    msg = "TEST"
    logger.bind(TEST1='TEST')
    logger.debug(msg, TEST='TEST')
    es_handler.flush()
    data = socket_data(socket)[0]
    assert data['message'] == msg
    assert data['levelname'] == logging.getLevelName(logging.DEBUG)
    assert 'TEST' in data
    assert data['TEST'] == 'TEST'
    assert 'TEST1' in data
    assert data['TEST1'] == 'TEST'
