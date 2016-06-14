import logging
import pytest


def test_tracing_by_function_if_enable(track_logger, handler):
    msg1 = 'TEST1'
    msg2 = 'TEST2'
    msg3 = 'TEST3'
    track_logger.setLevel(logging.INFO)
    track_logger.enable_tracking()
    track_logger.debug(msg1)
    track_logger.info(msg2)
    track_logger.disable_tracking()
    track_logger.debug(msg3)
    record = handler.pop()
    assert record.msg == msg2
    assert record.levelname == logging.getLevelName(logging.INFO)
    with pytest.raises(IndexError):
        handler.pop()


def test_tracing_by_function_if_enable_with_exc(track_logger, handler):
    msg1 = 'TEST1'
    msg2 = 'TEST2'
    msg3 = 'TEST3'
    track_logger.setLevel(logging.INFO)
    track_logger.enable_tracking()
    try:
        track_logger.debug(msg1)
        track_logger.info(msg2)
        raise Exception
    except Exception:
        track_logger.exit_with_exc()
    track_logger.debug(msg3)
    track_logger.disable_tracking()

    record_2 = handler.pop()
    record_1 = handler.pop()
    assert record_1.msg == msg1
    assert record_1.levelname == logging.getLevelName(logging.DEBUG)
    assert record_2.msg == msg2
    assert record_2.levelname == logging.getLevelName(logging.INFO)
    with pytest.raises(IndexError):
        handler.pop()


def test_tracing_by_context(track_logger, handler):
    msg1 = 'TEST1'
    msg2 = 'TEST2'
    msg3 = 'TEST3'
    track_logger.setLevel(logging.INFO)
    with track_logger.trace:
        track_logger.debug(msg1)
        track_logger.info(msg2)
    track_logger.debug(msg3)

    record = handler.pop()
    assert record.msg == msg2
    assert record.levelname == logging.getLevelName(logging.INFO)
    with pytest.raises(IndexError):
        handler.pop()


def test_tracing_by_context_with_exc(track_logger, handler):
    msg1 = 'TEST1'
    msg2 = 'TEST2'
    msg3 = 'TEST3'
    track_logger.setLevel(logging.INFO)
    try:
        with track_logger.trace:
            track_logger.debug(msg1)
            track_logger.info(msg2)
            raise Exception
    except Exception:
        pass
    track_logger.debug(msg3)

    record_2 = handler.pop()
    record_1 = handler.pop()
    assert record_1.msg == msg1
    assert record_1.levelname == logging.getLevelName(logging.DEBUG)
    assert record_2.msg == msg2
    assert record_2.levelname == logging.getLevelName(logging.INFO)
    with pytest.raises(IndexError):
        handler.pop()


def test_tracing_by_decorator(track_logger, handler):
    msg1 = 'TEST1'
    msg2 = 'TEST2'
    msg3 = 'TEST3'
    track_logger.setLevel(logging.INFO)

    @track_logger.trace
    def trace_func():
        track_logger.debug(msg1)
        track_logger.info(msg2)

    trace_func()
    track_logger.debug(msg3)

    record = handler.pop()
    assert record.msg == msg2
    assert record.levelname == logging.getLevelName(logging.INFO)
    with pytest.raises(IndexError):
        handler.pop()


def test_tracing_by_decorator_with_exc(track_logger, handler):
    msg1 = 'TEST1'
    msg2 = 'TEST2'
    msg3 = 'TEST3'
    track_logger.setLevel(logging.INFO)

    @track_logger.trace
    def trace_func():
        track_logger.debug(msg1)
        track_logger.info(msg2)
        raise Exception

    try:
        trace_func()
    except Exception:
        pass
    track_logger.debug(msg3)

    record_2 = handler.pop()
    record_1 = handler.pop()
    assert record_1.msg == msg1
    assert record_1.levelname == logging.getLevelName(logging.DEBUG)
    assert record_2.msg == msg2
    assert record_2.levelname == logging.getLevelName(logging.INFO)
    with pytest.raises(IndexError):
        handler.pop()
