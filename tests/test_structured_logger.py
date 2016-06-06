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


@pytest.fixture()
def struct_logger1(struct_logger):
    return struct_logger


@pytest.fixture()
def struct_logger2(struct_logger):
    return struct_logger


@pytest.mark.parametrize('level',
                         [logging.DEBUG,
                          logging.INFO,
                          logging.WARNING,
                          logging.CRITICAL,
                          logging.ERROR])
def test_context_singleton(level, struct_logger1, struct_logger2, handler):
    msg1 = "TEST1"
    msg2 = "TEST2"
    levelname = logging.getLevelName(level)
    struct_logger1.bind(TEST='TEST')
    level_mapper(struct_logger1, levelname)(msg1)
    level_mapper(struct_logger2, levelname)(msg2)

    record_2 = handler.pop()
    record_1 = handler.pop()

    assert record_1.msg == msg1
    assert record_2.msg == msg2
    assert 'TEST' in record_1.__dict__
    assert 'TEST' in record_2.__dict__
    assert record_1.TEST == 'TEST'
    assert record_2.TEST == 'TEST'
    assert id(struct_logger1) == id(struct_logger2)
