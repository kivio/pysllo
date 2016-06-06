import pytest
import logging


def level_mapper(obj, level):
    func_mapper = {
        'DEBUG': obj.debug,
        'INFO': obj.info,
        'WARNING': obj.warning,
        'CRITICAL': obj.critical,
        'ERROR': obj.error
    }
    return func_mapper[level]


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_logging(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    level_mapper(struct_logger, levelname)(msg)
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


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_string_format_msg(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST {}"
    sub = "SUB_TEST"
    level_mapper(struct_logger, levelname)(msg, sub)
    record = handler.pop()
    assert record.msg == msg
    assert sub in record.args


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_simple_extra(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    level_mapper(struct_logger, levelname)(msg, extra={'TEST': 'TEST'})
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
def test_extra_by_kwargs(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    level_mapper(struct_logger, levelname)(msg, TEST='TEST')
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
def test_bind_extras(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    struct_logger.bind(TEST='TEST')
    level_mapper(struct_logger, levelname)(msg)
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
def test_unbind_extras_by_name(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    struct_logger.bind(TEST='TEST')
    struct_logger.unbind('TEST')
    level_mapper(struct_logger, levelname)(msg)
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' not in record.__dict__


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_unbind_all_extras(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    struct_logger.bind(TEST='TEST')
    struct_logger.unbind()
    level_mapper(struct_logger, levelname)(msg)
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' not in record.__dict__


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_unbind_just_one_extras(level, struct_logger, handler):
    levelname = logging.getLevelName(level)
    msg = "TEST"
    struct_logger.bind(TEST='TEST', TEST1='TEST1')
    struct_logger.unbind('TEST')
    level_mapper(struct_logger, levelname)(msg)
    record = handler.pop()
    assert record.msg == msg
    assert 'TEST' not in record.__dict__
    assert 'TEST1' in record.__dict__
    assert record.TEST1 == 'TEST1'
