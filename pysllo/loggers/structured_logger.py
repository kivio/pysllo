# coding:utf-8

from logging import Logger


class StructuredLogger(Logger):
    """
    StructuredLogger is a class that make possible to add and bind additional
    information to logs as named parameters that extends functionality of
    extra parameter in default logger class

    To use it:
    import logging
    from pysllo.loggers import StructuredLogger
    logging.setLoggerClass(StructurredLogger)
    log = logging.getLogger('name')
    """
    _context = {}

    def _proper_extra(self, kwargs):
        extra = kwargs.pop('extra', {})
        exc_info = kwargs.pop('exc_info', None)
        extra.update(kwargs)
        extra.update(StructuredLogger._context)
        new_kwargs = {'extra': extra, 'exc_info': exc_info}
        return new_kwargs

    def _log(self, level, msg, args, **kwargs):
        kwargs = self._proper_extra(kwargs)
        Logger._log(self, level, msg, args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        copied from python 2.7.4 for compatibility with python <2.7.4
        """
        kwargs['exc_info'] = True
        self.error(msg, *args, **kwargs)

    def __contains__(self, item):
        return item in self._context

    def get(self, item, default=None):
        """
        Return value of item in context if exists
        :param item: name of context element to get
        :param default: default value if element is not in context
        :return:
        """
        return self._context.get(item, default)

    @staticmethod
    def bind(**kwargs):
        """
        Bind params as context to logger
        :param kwargs: list of named arguments
        :return:
        """
        StructuredLogger._context.update(kwargs)

    @staticmethod
    def unbind(*args):
        """
        Remove params from context by names, possible to give list of names
        :param args: names of context elements to remove
        :return:
        """
        if args:
            for arg in args:
                StructuredLogger._context.pop(arg)
        else:
            StructuredLogger._context = {}
