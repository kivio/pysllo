import datetime
import json


class LoggingJSONEncoder(json.JSONEncoder):
    """ encoder that supports datetime and time builtin types
    """

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return str(obj)  # str because of python3.x
        return super(LoggingJSONEncoder, self).default(obj)
