import pysllo.loggers as loggers

from pysllo.utils import LoggersFactory
from logging import Logger


def test_normal_logger():
    logger = LoggersFactory.make()
    assert issubclass(logger, Logger)
    assert not issubclass(logger, loggers.StructuredLogger)
    assert not issubclass(logger, loggers.PropagationLogger)
    assert not issubclass(logger, loggers.TrackingLogger)


def test_structured_logger():
    logger = LoggersFactory.make(structured_logger=True)
    assert issubclass(logger, Logger)
    assert issubclass(logger, loggers.StructuredLogger)
    assert not issubclass(logger, loggers.PropagationLogger)
    assert not issubclass(logger, loggers.TrackingLogger)


def test_propagation_logger():
    logger = LoggersFactory.make(propagation_logger=True)
    assert issubclass(logger, Logger)
    assert not issubclass(logger, loggers.StructuredLogger)
    assert issubclass(logger, loggers.PropagationLogger)
    assert not issubclass(logger, loggers.TrackingLogger)


def test_tracking_logger():
    logger = LoggersFactory.make(tracking_logger=True)
    assert issubclass(logger, Logger)
    assert not issubclass(logger, loggers.StructuredLogger)
    assert issubclass(logger, loggers.PropagationLogger)
    assert issubclass(logger, loggers.TrackingLogger)


def test_mixed_logger():
    logger = LoggersFactory.make(
        tracking_logger=True,
        propagation_logger=True,
        structured_logger=True
    )
    assert issubclass(logger, Logger)
    assert issubclass(logger, loggers.StructuredLogger)
    assert issubclass(logger, loggers.PropagationLogger)
    assert issubclass(logger, loggers.TrackingLogger)
