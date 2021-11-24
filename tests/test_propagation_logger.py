import pytest
import logging


def test_forcing_level_by_level_value(propagation_logger, handler):
    msg = "TEST"
    propagation_logger.setLevel(logging.INFO)
    propagation_logger.force_level(logging.DEBUG)
    propagation_logger.debug(msg)
    record = handler.pop()

    assert record.msg == msg
    assert record.levelname == logging.getLevelName(logging.DEBUG)
    with pytest.raises(IndexError):
        handler.pop()


def test_forcing_level_by_level_name(propagation_logger, handler):
    msg = "TEST"
    propagation_logger.setLevel(logging.INFO)
    propagation_logger.force_level(logging.getLevelName(logging.DEBUG))
    propagation_logger.debug(msg)
    record = handler.pop()
    assert record.msg == msg
    assert record.levelname == logging.getLevelName(logging.DEBUG)
    with pytest.raises(IndexError):
        handler.pop()


def test_level_propagation(propagation_logger, handler):
    msg1 = "TEST1"
    msg2 = "TEST2"
    propagation_logger.set_propagation(True)
    propagation_logger.setLevel(logging.INFO)

    def test_second_level():
        propagation_logger.debug(msg2)

    @propagation_logger.level_propagation(logging.DEBUG)
    def test_first_level():
        propagation_logger.debug(msg1)
        test_second_level()

    test_first_level()
    test_second_level()

    record2 = handler.pop()
    record1 = handler.pop()
    assert record1.levelname == logging.getLevelName(logging.DEBUG)
    assert record2.levelname == logging.getLevelName(logging.DEBUG)
    with pytest.raises(IndexError):
        handler.pop()


def test_reset_level(propagation_logger, handler):
    msg = "TEST"
    propagation_logger.setLevel(logging.INFO)
    propagation_logger.force_level(logging.getLevelName(logging.DEBUG))
    propagation_logger.reset_level()
    propagation_logger.debug(msg)
    with pytest.raises(IndexError):
        handler.pop()


def test_forcing_level_with_kwargs_by_level(propagation_logger, handler):
    msg1 = "TEST1"
    msg2 = "TEST2"
    propagation_logger.setLevel(logging.INFO)
    propagation_logger.force_level(logger_1=logging.DEBUG)
    additional_logger = logging.getLogger('logger_1')
    additional_logger.setLevel(logging.INFO)
    additional_logger.addHandler(handler)
    propagation_logger.debug(msg1)
    additional_logger.debug(msg2)
    record = handler.pop()
    assert record.msg == msg2
    assert record.levelname == logging.getLevelName(logging.DEBUG)
    with pytest.raises(IndexError):
        handler.pop()


def test_forcing_level_with_kwargs_by_level(propagation_logger, handler):
    msg1 = "TEST1"
    msg2 = "TEST2"
    propagation_logger.setLevel(logging.INFO)
    propagation_logger.force_level(logger_1="DEBUG")
    additional_logger = logging.getLogger('logger_1')
    additional_logger.setLevel(logging.INFO)
    additional_logger.addHandler(handler)
    propagation_logger.debug(msg1)
    additional_logger.debug(msg2)
    record = handler.pop()
    assert record.msg == msg2
    assert record.levelname == logging.getLevelName(logging.DEBUG)
    with pytest.raises(IndexError):
        handler.pop()


def test_forcing_level_by_dict(propagation_logger, handler):
    propagation_logger.reset_level()
    msg1 = "TEST1"
    msg2 = "TEST2"
    propagation_logger.setLevel(logging.INFO)
    levels = {
            'logger_1': logging.DEBUG
        }
    propagation_logger.force_level(levels)
    additional_logger = logging.getLogger('logger_1')
    additional_logger.setLevel(logging.INFO)
    additional_logger.addHandler(handler)
    propagation_logger.debug(msg1)
    additional_logger.debug(msg2)
    record = handler.pop()
    assert record.msg == msg2
    assert record.levelname == logging.getLevelName(logging.DEBUG)
    with pytest.raises(IndexError):
        handler.pop()


def test_forcing_level_without_args_and_kwargs(propagation_logger, handler):
    with pytest.raises(TypeError) as exc_info:
        propagation_logger.force_level()
    assert '0 given' in str(exc_info.value)


def test_forcing_level_with_too_many_args(propagation_logger, handler):
    with pytest.raises(TypeError) as exc_info:
        propagation_logger.force_level(logging.DEBUG, logging.DEBUG)
    assert '2 given' in str(exc_info.value)
