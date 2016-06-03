import pytest
import logging


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_logging(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    struct_logger.__getattribute__(levelname.lower())(msg)
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == levelname


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_log(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    struct_logger.log(level, msg)
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == levelname


def test_simple_exception(struct_logger, handler):
    msg = "TEST"
    e = None
    try:
        e = Exception
        raise e
    except Exception:
        struct_logger.exception(msg)
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == logging.getLevelName(logging.ERROR)
    assert record.exc_info[0] == e


def test_simple_string_format_msg(struct_logger, handler):
    msg = "TEST {}"
    sub = "SUB_TEST"
    struct_logger.debug(msg, sub)
    record = handler.pop()
    assert record.msg == msg
    assert sub in record.args


def test_simple_extra(struct_logger, handler):
    msg = "TEST"
    struct_logger.debug(msg, extra={'TEST': 'TEST'})
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' in record.__dict__
    assert record.TEST == 'TEST'
