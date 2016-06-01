import logging


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
