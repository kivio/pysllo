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

    @staticmethod
    def bind(**kwargs):
        StructuredLogger._context.update(kwargs)
