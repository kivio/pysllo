from logging import Logger


class LoggersFactory(object):
    """
    LoggersFactory is static helper that makes combined Logger class with
    possible maximum features that you want to use.

    To use it:

    >>> MixedLogger = LoggersFactory.make(
    >>>    tracking_logger=True,
    >>>    structured_logger=True
    >>> )
    >>> logging.setLoggerClass(MixedLogger)
    >>> log = logging.getLogger('test')
    """

    @staticmethod
    def make(structured_logger=False,
             propagation_logger=False,
             tracking_logger=False):
        """
        Method based on your choices create on class that support all chooses
        functions.

        :param structured_logger: (bool) on/off structured logger features
        :param propagation_logger: (bool) on/off propagation possibility
        :param tracking_logger: (bool) on/off tracking function
        :return: (MixedLogger class) combined logger class
        """

        class XYZ(object):
            pass

        # fix for python 2.6 compatibility
        import sys
        if sys.version.startswith('2.6'):  # pragma: no cover
            setattr(Logger.__bases__[0], '__mro__', object)

        cls_list = []
        if structured_logger:
            from ..loggers import StructuredLogger
            cls_list.append(StructuredLogger)
        if tracking_logger:
            from ..loggers import TrackingLogger
            cls_list.append(TrackingLogger)
        if propagation_logger:
            from ..loggers import TrackingLogger
            if TrackingLogger not in cls_list:
                from ..loggers import PropagationLogger
                cls_list.append(PropagationLogger)
        if not len(cls_list):
            cls_list.append(Logger)
        cls_list.append(XYZ)
        return type('MixedLogger', tuple(cls_list), {})
