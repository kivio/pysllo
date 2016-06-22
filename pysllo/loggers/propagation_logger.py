# coding:utf-8

import logging

from functools import wraps
from logging import Logger


class PropagationLogger(Logger):
    """
    PropagationLogger is Logger class that makes possible to propagate
    logging level across block of code, especially function, context or
    manually your own.

    To use it:
    import logging
    from pysllo.loggers import PropagationLogger
    logging.setLoggerClass(PropagationLogger)
    log = logging.getLogger('name')
    """

    _forcing = {}
    _global_propagation_level = logging.NOTSET

    def __init__(self, name, level=logging.NOTSET, propagation=False):
        Logger.__init__(self, name, level)
        self._level_propagation = propagation

    def set_propagation(self, propagation=True):
        """
        Function that enable/disable propagation level functionality
        :param propagation: bool
        :return: None
        """
        if isinstance(propagation, bool):
            self._level_propagation = propagation

    def getEffectiveLevel(self):
        """
        Get the effective level for this logger.

        Loop through this logger and its parents in the logger hierarchy,
        looking for a non-zero logging level. Return the first one found.

        Accepting propagation configuration as first priority.
        """
        if self.name in PropagationLogger._forcing:
            level = PropagationLogger._forcing[self.name]
            if isinstance(level, int):
                return level
            else:
                return logging.getLevelName(level)
        if PropagationLogger._global_propagation_level != logging.NOTSET:
            return PropagationLogger._global_propagation_level
        return Logger.getEffectiveLevel(self)

    @staticmethod
    def reset_level():
        """
        Resetting level of propagation
        :return:
        """
        PropagationLogger._global_propagation_level = logging.NOTSET

    @staticmethod
    def level_propagation(level):
        """
        Decorator that give propagation functionality to decorated function
        :param level: int - logging level
        :return:
        """
        def decor(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                PropagationLogger.force_level(level)
                result = f(*args, **kwargs)
                PropagationLogger.reset_level()
                return result
            return decorated
        return decor

    @staticmethod
    def force_level(*args, **kwargs):
        """
        Function that make possible to force level value for specific loggers
        :param args: level name or dict with configuration
        :param kwargs: name of logger and value
        :return:
        """
        if len(args) > 1:
            raise TypeError("force_level() takes exactly one argument "
                            "or named arguments ({0} given)".format(len(args)))

        elif len(args) == 1:
            if isinstance(args[0], int):
                PropagationLogger._global_propagation_level = args[0]
            elif isinstance(args[0], "".__class__):
                PropagationLogger._global_propagation_level = \
                    logging.getLevelName(args[0])
            elif isinstance(args[0], dict):
                PropagationLogger._forcing = args[0]
        else:
            if kwargs:
                PropagationLogger._forcing = kwargs
            else:
                raise TypeError("force_level() takes exactly one "
                                "argument or named arguments (0 given)")
