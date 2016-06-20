import logging
import json


class TestHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self._records = []

    def emit(self, record):
        self._records.append(record)

    def pop(self):
        return self._records.pop()

    def flush(self):
        self._records = []

    def __len__(self):
        return len(self._records)


def level_mapper(obj, level):
    func_mapper = {
        'DEBUG': obj.debug,
        'INFO': obj.info,
        'WARNING': obj.warning,
        'CRITICAL': obj.critical,
        'ERROR': obj.error
    }
    return func_mapper[level]


class TestSocket(object):

    def __init__(self):
        self._records = []

    def sendto(self, data, connection):
        self._records.append((data, connection))

    def send(self, data):
        self._records.append(data)

    def pop(self):
        return self._records.pop()

    def pop_with_connection(self):
        return self._records.pop()

    def flush(self):
        self._records = []


def socket_data(socket):
    record = socket.pop()
    result = []
    for c in record:
        data = c.split("\n")
        result.append(json.loads(data[1]))
    return result
