from logging import Logger
from ..loggers import StructuredLogger
from ..loggers import PropagationLogger
from ..loggers import TrackingLogger


class LoggersFactory(object):

    @staticmethod
    def make(structured_logger=False,
             propagation_logger=False,
             tracking_logger=False):

        class XYZ(object):
            pass

        # fix for python 2.6 compatibility
        import sys
        if sys.version.startswith('2.6'):  # pragma: no cover
            setattr(Logger.__bases__[0], '__mro__', object)

        cls_list = []
        if structured_logger:
            cls_list.append(StructuredLogger)
        if tracking_logger:
            cls_list.append(TrackingLogger)
        if propagation_logger:
            if TrackingLogger not in cls_list:
                cls_list.append(PropagationLogger)
        if not len(cls_list):
            cls_list.append(Logger)
        cls_list.append(XYZ)
        return type('MixedLogger', tuple(cls_list), {})
