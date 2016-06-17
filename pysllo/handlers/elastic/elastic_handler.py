import datetime
import logging
import sys

from pysllo.utils.udp_buffer import UDPBuffer


class ElasticSearchUDPHandler(logging.Handler):
    _buffer = []
    _current_size = 0
    _limit = 0
    _backup_enabled = False
    _backup_path = "./"
    _doc_type = 'logs'

    def __init__(self, connections,
                 level=logging.NOTSET, name='logs', limit=9000, backup=False):
        logging.Handler.__init__(self, level)
        self._connection = UDPBuffer(connections, limit=limit)
        ElasticSearchUDPHandler._doc_type = name
        ElasticSearchUDPHandler._limit = limit
        ElasticSearchUDPHandler._backup_enabled = backup

    @staticmethod
    def set_backup_path(path):
        ElasticSearchUDPHandler._backup_path = \
            path + ("/" if not path.endswith('/') else "")

    @staticmethod
    def enable_backup():
        ElasticSearchUDPHandler._backup_enabled = True

    @staticmethod
    def disable_backup():
        ElasticSearchUDPHandler._backup_enabled = False

    @staticmethod
    def set_limit(limit):  # pragma: no cover
        ElasticSearchUDPHandler._limit = limit

    @staticmethod
    def index():
        return '-'.join([
            ElasticSearchUDPHandler._doc_type,
            datetime.date.today().strftime('%Y-%m-%d')
        ])

    def emit(self, record):
        msg = self.format(record)
        data_size = sys.getsizeof(msg, 0)

        if ElasticSearchUDPHandler._current_size + data_size > self._limit:
            self.flush()

        ElasticSearchUDPHandler._current_size += data_size
        ElasticSearchUDPHandler._buffer.append(msg)

    def flush(self):
        self.acquire()
        payload = ElasticSearchUDPHandler._buffer
        self._connection.send(payload)
        self.backup(payload)
        ElasticSearchUDPHandler._current_size = 0
        ElasticSearchUDPHandler._buffer = []
        self.release()

    def backup(self, data):
        if self._backup_enabled:
            path = self._backup_path + self.index()
            with open(path, 'a') as out_file:
                out_file.write('\n'.join(data))

    def close(self):
        self.flush()
