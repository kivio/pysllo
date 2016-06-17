import logging
import json
import pytest

from pysllo.formatters.json_formatter import JsonFormatter
from pysllo.handlers import ElasticSearchUDPHandler
from tests.utils import TestSocket


@pytest.fixture()
def socket():
    return TestSocket()


@pytest.fixture()
def es_handler(socket):
    host, port = 'localhost', 9000
    handler = ElasticSearchUDPHandler([(host, port)], limit=1000)
    handler._connection = socket
    formatter = JsonFormatter(limit=1000)
    handler.setFormatter(formatter)
    return handler


@pytest.fixture()
def es_logger(es_handler):
    log = logging.getLogger('test')
    log.setLevel(logging.DEBUG)
    log.addHandler(es_handler)
    return log


def socket_data(socket):
    record = socket.pop()
    result = []
    for c in record:
        data = c.split("\n")
        result.append(json.loads(data[1]))
    return result


def test_connection(es_logger, es_handler, socket):
    msg = "TEST"
    es_logger.debug(msg)
    es_handler.flush()
    data = socket_data(socket)[0]
    assert data['message'] == msg
    assert data['levelname'] == logging.getLevelName(logging.DEBUG)


def test_not_backup(tmpdir, es_handler, es_logger, socket):
    msg = "TEST"
    path = 'es_backup'
    tmpdir.mkdir(path)
    backup_path = tmpdir.join(path)
    es_handler.set_backup_path(str(backup_path))
    es_logger.debug(msg)
    es_handler.flush()
    data = socket_data(socket)[0]
    assert data['message'] == msg
    assert data['levelname'] == logging.getLevelName(logging.DEBUG)
    backup_file = backup_path.join(es_handler.index())
    assert not backup_file.check()


def test_backup_disabling(tmpdir, es_handler, es_logger, socket):
    msg = "TEST"
    path = 'es_backup'
    tmpdir.mkdir(path)
    backup_path = tmpdir.join(path)
    es_handler.set_backup_path(str(backup_path))
    es_handler.enable_backup()
    es_handler.disable_backup()
    es_logger.debug(msg)
    es_handler.flush()
    data = socket_data(socket)[0]
    assert data['message'] == msg
    assert data['levelname'] == logging.getLevelName(logging.DEBUG)
    backup_file = backup_path.join(es_handler.index())
    assert not backup_file.check()


def test_backup_file(tmpdir, es_handler, es_logger, socket):
    msg = "TEST"
    path = 'es_backup'
    tmpdir.mkdir(path)
    backup_path = tmpdir.join(path)
    es_handler.set_backup_path(str(backup_path))
    es_handler.enable_backup()
    es_logger.debug(msg)
    es_handler.flush()
    data = socket_data(socket)[0]
    assert data['message'] == msg
    assert data['levelname'] == logging.getLevelName(logging.DEBUG)
    backup_file = backup_path.join(es_handler.index())
    assert backup_file.check()


def test_close_handler(es_logger, es_handler, socket):
    msg = "TEST"
    es_logger.debug(msg)
    es_handler.close()
    data = socket_data(socket)[0]
    assert data['message'] == msg
    assert data['levelname'] == logging.getLevelName(logging.DEBUG)
