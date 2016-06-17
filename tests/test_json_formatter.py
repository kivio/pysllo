# coding:utf-8

import pytest
import logging
import datetime

from pysllo.formatters.json_formatter import JsonFormatter


@pytest.fixture()
def formatter():
    return JsonFormatter(name='test', limit=1000)


def test_simple_msg(formatter):
    msg = "TEST"
    record = logging.makeLogRecord({'msg': msg})
    result = formatter.format(record)
    find = '"msg": "{0}"'.format(msg)
    assert find in result


def test_too_long_msg(formatter):
    msg = "TEST"*100000
    record = logging.makeLogRecord({'msg': msg})
    result = formatter.format(record)
    find = '"msg": "{0}"'.format(msg)
    assert find in result


def test_too_long_unicode_msg(formatter):
    msg = u"łążćóń"*100000
    record = logging.makeLogRecord({'msg': msg})
    result = formatter.format(record)
    find = u'"msg": "{0}"'.format(msg)
    assert find not in result
    assert "msg" in result


def test_msg_with_datetime(formatter):
    msg = "TEST"
    test_date = datetime.datetime(2010, 10, 10, 10, 10)
    record = logging.makeLogRecord({'msg': msg, 'date': test_date})
    result = formatter.format(record)
    find = '"msg": "{0}"'.format(msg)
    assert find in result
    find = '"date": "{0}"'.format(str(test_date))
    assert find in result


def test_msg_with_unserializable_obj(formatter):
    msg = "TEST"

    class TestCls(object):
        pass

    test_obj = TestCls()
    record = logging.makeLogRecord({'msg': msg, 'obj': test_obj})
    with pytest.warns(UserWarning):
        result = formatter.format(record)
    assert '"error": "unable to serialize"' in result


def test_msg_with_bad_formatting(formatter):
    msg = "%s"
    record = logging.makeLogRecord({'msg': msg, 'args': (1, 2, 3)})
    result = formatter.format(record)
    assert '''"message": "Couldn't parse arguments to message"''' in result


def test_msg_with_exception(formatter):
    import sys
    try:
        raise Exception
    except Exception:
        record = logging.makeLogRecord({'exc_info': sys.exc_info()})
        result = formatter.format(record)

    find = '"exc_class": "{0}"'.format(type(Exception()))
    assert find in result
    assert 'exc_info' not in result


def test_skipping_msg(formatter):
    record = logging.makeLogRecord({'name': 'elasticsearch'})
    result = formatter.format(record)

    assert result == ''
