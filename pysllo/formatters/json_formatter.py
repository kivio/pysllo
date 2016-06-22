import logging
import json
import copy
import traceback
import math
import warnings
import datetime
import sys
from uuid import uuid1
from pysllo.utils.json_encoder import LoggingJSONEncoder

MTL_OVER_SIZE = sys.getsizeof(", 'ES_MTL' : true,", 0)
logging_json_encoder = LoggingJSONEncoder()


class JsonFormatter(logging.Formatter):
    """
    JsonFormatter give logging possibility to convert your logs into JSON
    records that give possibility to save it in document based databases
    """

    _limit = 9000
    _doc_type = 'logs'

    def __init__(self, name='logs', limit=9000):
        JsonFormatter._doc_type = name
        JsonFormatter._limit = limit

    @staticmethod
    def format_exception(ei):
        """
        This method is helper that convert exception information into
        dict with specific data
        :param ei: exception info
        :return:
        """
        exc_class, exc_obj, trace = ei
        exc_class = repr(exc_class)
        trace = "".join(traceback.format_tb(trace))
        return {
            'traceback': trace,
            'exc_class': exc_class
        }

    @staticmethod
    def _jsonify_message(index, data):
        if 'exc_info' in data and data['exc_info']:
            data.update(JsonFormatter.format_exception(data['exc_info']))
            del data['exc_info']
        try:
            message = '\n'.join([
                logging_json_encoder.encode(index),
                logging_json_encoder.encode(data),
                '',  # it's here to add \n at end of the message
            ])
        except TypeError as e:
            message = '\n'.join([
                json.dumps(index),
                json.dumps({"error": "unable to serialize"}),
                '',
            ])
            warnings.warn('cannot serialize: {0}'.format(e))
        except UnicodeDecodeError as e:  # pragma: no cover
            message = '\n'.join([
                json.dumps(index),
                json.dumps({"error": "unable to decode"}),
                '',
            ])
            warnings.warn('cannot decode as utf8: {0}'.format(e))
        return message

    # no cover - support different versions of python
    @staticmethod
    def _count_to_remove_chars(over_limit, msg):  # pragma: no cover
        to_remove_chars_count = 0
        if sys.version_info[0] == 3:
            # size of one character in string class in python 3.x is 2
            to_remove_chars_count = int(math.ceil(over_limit / 2))
        else:
            if isinstance(msg, unicode):
                # size of one character in unicode class in python 2.x is 4
                to_remove_chars_count = int(math.ceil(over_limit / 4))
            elif isinstance(msg, str):
                # size of one character in str in python 2.x in 1
                to_remove_chars_count = over_limit
        return int(math.fabs(to_remove_chars_count))

    @staticmethod
    def _truncate_too_long_message(index, data, size, limit):
        # is added to result when we have data over limit
        over_limit = (size - limit) + MTL_OVER_SIZE
        to_remove_chars_count = JsonFormatter._count_to_remove_chars(
            over_limit, data['message'])
        data['message'] = data['message'][:-to_remove_chars_count]
        data['ES_MTL'] = True
        return JsonFormatter._jsonify_message(index, data)

    @staticmethod
    def serialize_record(record, index_data, limit):
        """
        This method transfer and processes log record into JSON object
        :param record:
        :param index_data:
        :param limit:
        :return:
        """
        if record.name in ('elasticsearch', 'urllib3.connectionpool'):
            return ''

        data = copy.copy(record.__dict__)
        data['@timestamp'] = datetime.datetime.utcnow().isoformat() + 'Z'

        # The primary information is passed in msg and args,
        # which are combined using msg % args to create the message field
        # of the record.

        try:
            if ('message' not in data or data['message'] == "")\
                    and 'msg' in data and 'args' in data:
                data['message'] = data['msg'] % data['args']
        except Exception:
            data['message'] = "Couldn't parse arguments to message"

        ignored = (
            'process',
            'relativeCreated',
            'args',
            'thread',
            'created',
            'threadName',
            'msecs',
            'levelno',
            'processName',
        )

        for ignore in ignored:
            data.pop(ignore, None)

        full_index = dict(index_data)
        full_index['index']['_id'] = str(uuid1())

        message = JsonFormatter._jsonify_message(full_index, data)
        size = sys.getsizeof(message, 0)

        if size > (limit - MTL_OVER_SIZE):
            message = JsonFormatter._truncate_too_long_message(
                full_index, data, size, limit)

        return message

    @staticmethod
    def index():
        """
        Special method that create identifier for today logs
        :return: dict
        """
        return '-'.join([
            JsonFormatter._doc_type,
            datetime.date.today().strftime('%Y-%m-%d')
        ])

    def format(self, record):
        """
        It's standard logging method to format record to JSON
        :param record:
        :return:
        """
        index_data = {
            'index': {
                '_index': self.index(),
                '_type': self._doc_type
            }
        }
        return self.serialize_record(record, index_data=index_data,
                                     limit=self._limit)
