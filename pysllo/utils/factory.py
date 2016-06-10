from logging import Logger
from ..loggers import StructuredLogger
from ..loggers import PropagationLogger
from ..loggers import TrackingLogger


class LoggersFactory(object):

    @staticmethod
    def make(structured_logger=False,
             propagation_logger=False,
             tracking_logger=False):

        # fix for python 2.6 compatibility
        class XYZ(object):
            pass

        import sys
        if sys.version_info.major == 2 and sys.version_info.minor == 6:
            setattr(Logger.__bases__[0], '__mro__', object)

        cls_list = []
        if structured_logger:
            cls_list.append(StructuredLogger)
        if propagation_logger:
            cls_list.append(PropagationLogger)
        if tracking_logger:
            cls_list.append(TrackingLogger)
        if not len(cls_list):
            cls_list.extend([Logger, XYZ])
        return type('MixedLogger', tuple(cls_list), {})
