import pytest
import logging


from .utils import level_mapper


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_logging(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    level_mapper(structured_logger, levelname)(msg)
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == levelname


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_log(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    structured_logger.log(level, msg)
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == levelname


def test_simple_exception(structured_logger, handler):
    msg = "TEST"
    e = None
    try:
        e = Exception
        raise e
    except Exception:
        structured_logger.exception(msg)
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == logging.getLevelName(logging.ERROR)
    assert record.exc_info[0] == e


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_string_format_msg(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST {}"
    sub = "SUB_TEST"
    level_mapper(structured_logger, levelname)(msg, sub)
    record = handler.pop()
    assert record.msg == msg
    assert sub in record.args


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_extra(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    level_mapper(structured_logger, levelname)(msg, extra={'TEST': 'TEST'})
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' in record.__dict__
    assert record.TEST == 'TEST'


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_extra_by_kwargs(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    level_mapper(structured_logger, levelname)(msg, TEST='TEST')
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' in record.__dict__
    assert record.TEST == 'TEST'


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_bind_extras(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    structured_logger.bind(TEST='TEST')
    level_mapper(structured_logger, levelname)(msg)
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' in record.__dict__
    assert record.TEST == 'TEST'


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_unbind_extras_by_name(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    structured_logger.bind(TEST='TEST')
    structured_logger.unbind('TEST')
    level_mapper(structured_logger, levelname)(msg)
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' not in record.__dict__


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_unbind_all_extras(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    structured_logger.bind(TEST='TEST')
    structured_logger.unbind()
    level_mapper(structured_logger, levelname)(msg)
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' not in record.__dict__


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_unbind_just_one_extras(level, structured_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    structured_logger.bind(TEST='TEST', TEST1='TEST1')
    structured_logger.unbind('TEST')
    level_mapper(structured_logger, levelname)(msg)
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' not in record.__dict__
    assert 'TEST1' in record.__dict__
    assert record.TEST1 == 'TEST1'


@pytest.fixture()
def structured_logger1(structured_logger):
    return structured_logger


@pytest.fixture()
def structured_logger2(structured_logger):
    return structured_logger


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_context_singleton(level, structured_logger1,
                           structured_logger2, handler):
    msg1 = "TEST1"
    msg2 = "TEST2"
    levelname = logging.getLevelName(level)
    structured_logger1.bind(TEST='TEST')
    level_mapper(structured_logger1, levelname)(msg1)
    level_mapper(structured_logger2, levelname)(msg2)

    record_2 = handler.pop()
    record_1 = handler.pop()

    assert record_1.msg == msg1
    assert record_2.msg == msg2
    assert 'TEST' in record_1.__dict__
    assert 'TEST' in record_2.__dict__
    assert record_1.TEST == 'TEST'
    assert record_2.TEST == 'TEST'
    assert id(structured_logger1) == id(structured_logger2)


def test_contain_extras(structured_logger):
    structured_logger.bind(TEST='TEST')
    assert 'TEST' in structured_logger


def test_get_from_context(structured_logger):
    structured_logger.bind(TEST='TEST')
    assert 'TEST' in structured_logger
    assert structured_logger.get('TEST') == 'TEST'
    assert structured_logger.get('TEST2') is None
    assert structured_logger.get('TEST3', 'NO') == 'NO'


def test_level_exception_with_extra_args(structured_logger, handler):
    msg = "TEST"
    e = None
    try:
        e = Exception()
        raise e
    except Exception:
        structured_logger.exception(msg, TEST='TEST')
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == logging.getLevelName(logging.ERROR)
    assert isinstance(e, record.exc_info[0])
    assert 'TEST' in record.__dict__
    assert record.TEST == 'TEST'
