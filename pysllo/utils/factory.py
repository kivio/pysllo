from logging import Logger
from ..loggers import StructuredLogger
from ..loggers import PropagationLogger
from ..loggers import TrackingLogger


class LoggersFactory(object):

    @staticmethod
    def make(structured_logger=False,
             propagation_logger=False,
             tracking_logger=False):
        cls_list = [Logger]
        if structured_logger:
            cls_list.append(StructuredLogger)
        elif propagation_logger:
            cls_list.append(PropagationLogger)
        elif tracking_logger:
            cls_list.append(TrackingLogger)
        return type('MixedLogger', cls_list, {})
