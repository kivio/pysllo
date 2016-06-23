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

    >>> import logging
    >>> from pysllo.loggers import PropagationLogger
    >>> logging.setLoggerClass(PropagationLogger)
    >>> log = logging.getLogger('name')

    Most popular usage of this logger is to propagate level between functions
    used in some scope.
    For example:

    >>> logger.set_propagation(True)
    >>> logger.setLevel(logging.INFO)
    >>>
    >>> def test_second_level():
    >>>    logger.debug("msg2")
    >>>
    >>> @logger.level_propagation(logging.DEBUG)
    >>> def test_first_level():
    >>>    logger.debug("msg1")
    >>>    test_second_level()
    >>>
    >>> test_first_level()
    >>> test_second_level()

    In this case instead of globally configured level INFO if function
    `test_second_level` is used in scope where propagation is enabled
    log from `test_second_level` will be pushed to handler ignoring
    global configuration. In second run of this function without propagation
    log on level DEBUG from that function will be dropped because there is
    normal configuration scope.
    """

    _forcing = {}
    _global_propagation_level = logging.NOTSET

    def __init__(self, name, level=logging.NOTSET, propagation=False):
        """
        Used automatically by `getLogger` but if you use config file,
        you can configure propagation from start which is fine option

        :param name: (str) logger name
        :param level: (int) logging level
        :param propagation: (bool) on/off propagation from start
        """
        Logger.__init__(self, name, level)
        self._level_propagation = propagation

    def set_propagation(self, propagation=True):
        """
        Function that enable/disable propagation level functionality

        :param propagation: (bool) make propagation on/off
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
        """
        PropagationLogger._global_propagation_level = logging.NOTSET

    @staticmethod
    def level_propagation(level):
        """
        Decorator that give propagation functionality to decorated function

        :param level: (int) logging level
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

        :param args: (str or dict) level name or configuration for more levels
        :param kwargs: (dict) name of logger and value as elements
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
