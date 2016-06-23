import datetime
import logging
import sys

from pysllo.utils.udp_buffer import UDPBuffer


class ElasticSearchUDPHandler(logging.Handler):
    """
        ElasticSearchUDPHandler is a logging handler that makes possible
        to send your logs to ElasticSearch cluster.

        To do that is used UDP connection, it's required to configure
        UDP bulk insert in your Elastic cluster.
        Another requirement is to use `pysllo.formatters.JsonFormatter` or other
        JSON formatter for that handler because default ElasticSearch Bulk
        format is list of JSON objects.

        For more information about this configuration see elastic page about
        UDP messages `here
        <https://www.elastic.co/guide/en/logstash/current/plugins-inputs-udp.html>`_.

        To use this handler just setup:

        >>> host, port = 'localhost', 9000
        >>> handler = ElasticSearchUDPHandler([(host, port)])
        >>> formatter = JsonFormatter()
        >>> handler.setFormatter(formatter)
        >>> log = logging.getLogger('test')
        >>> log.setLevel(logging.DEBUG)
        >>> log.addHandler(handler)

    """
    _buffer = []
    _current_size = 0
    _limit = 0
    _backup_enabled = False
    _backup_path = "./"
    _doc_type = 'logs'

    def __init__(self, connections,
                 level=logging.NOTSET, name='logs', limit=9000, backup=False):
        """
        Configure most important thing to setting this handler, list of
        connections is required, you can set more than one them round robin
        algorithm will be used to make next connections

        :param connections: (tuple or list) list of tuples with \
        server address and port
        :param level: (int) logging level
        :param name: (str) logger name
        :param limit: (int) byte size of buffer, after this limit buffer is \
        pushed to elastic cluster
        :param backup: on/off backup
        """
        logging.Handler.__init__(self, level)
        self._connection = UDPBuffer(connections, limit=limit)
        ElasticSearchUDPHandler._doc_type = name
        ElasticSearchUDPHandler._limit = limit
        ElasticSearchUDPHandler._backup_enabled = backup

    @staticmethod
    def set_backup_path(path):
        """
        Set path to backup files

        :param path: (str) unix path
        """
        ElasticSearchUDPHandler._backup_path = \
            path + ("/" if not path.endswith('/') else "")

    @staticmethod
    def enable_backup():
        """
        Enable backup functionality that make possible to make logs sending
        secure in situation of loosing connection.
        """
        ElasticSearchUDPHandler._backup_enabled = True

    @staticmethod
    def disable_backup():
        """
        Disable backup functionality
        """
        ElasticSearchUDPHandler._backup_enabled = False

    @staticmethod
    def set_limit(limit):  # pragma: no cover
        """
        Set limit value, limit is size of buffer to store messages, after
        make this buffer full all messages will be send.
        It's important to make there good number to make sure that you don't
        have too many connections to DB and to have too big snap of messages
        that can make delay's on real time dashboards

        :param limit: (int) number of bytes
        """
        ElasticSearchUDPHandler._limit = limit

    @staticmethod
    def index():
        """
        Special method that create identifier for today logs

        :return: (dict)
        """
        return '-'.join([
            ElasticSearchUDPHandler._doc_type,
            datetime.date.today().strftime('%Y-%m-%d')
        ])

    def emit(self, record):
        """
        Is standard logging Handler method that send message to receiver, in
        this case message is saved in buffer

        :param record: (LogRecord) - record to send
        """
        msg = self.format(record)
        data_size = sys.getsizeof(msg, 0)

        if ElasticSearchUDPHandler._current_size + data_size > self._limit:
            self.flush()

        ElasticSearchUDPHandler._current_size += data_size
        ElasticSearchUDPHandler._buffer.append(msg)

    def flush(self):
        """
        Method to send buffered messages to cluster
        """
        self.acquire()
        payload = ElasticSearchUDPHandler._buffer
        self._connection.send(payload)
        self.backup(payload)
        ElasticSearchUDPHandler._current_size = 0
        ElasticSearchUDPHandler._buffer = []
        self.release()

    def backup(self, data):
        """
        Method that save messages to backup if this functionality is enabled

        :param data: (str) - string version of buffered data
        """
        if self._backup_enabled:
            path = self._backup_path + self.index()
            with open(path, 'a') as out_file:
                out_file.write('\n'.join(data))

    def close(self):
        """
        Tidy up any resources used by the handler.

        This version removes the handler from an internal map of handlers,
        _handlers, which is used for handler lookup by name. Subclasses
        should ensure that this gets called from overridden close()
        methods.
        """
        self.flush()
