# coding:utf-8

from logging import Logger


class StructuredLogger(Logger):
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
        copied from python 2.7.4 for compatiblity with python <2.7.4
        """
        kwargs['exc_info'] = True
        self.error(msg, *args, **kwargs)

    def __contains__(self, item):
        return item in self._context

    def get(self, item, default=None):
        return self._context.get(item, default)

    @staticmethod
    def bind(**kwargs):
        StructuredLogger._context.update(kwargs)

    @staticmethod
    def unbind(*args):
        if args:
            for arg in args:
                StructuredLogger._context.pop(arg)
        else:
            StructuredLogger._context = {}
