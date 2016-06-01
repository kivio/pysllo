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
