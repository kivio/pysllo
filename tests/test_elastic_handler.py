import logging

from tests.utils import socket_data


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
