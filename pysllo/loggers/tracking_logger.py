# coding:utf-8
import logging

from .propagation_logger import PropagationLogger
from ..utils.tracer import Tracer, TraceContext


class TrackingLogger(PropagationLogger):

    _tracer = Tracer()
    _is_tracking_enable = False

    def __init__(self, name, level=logging.NOTSET, propagation=False):
        PropagationLogger.__init__(self, name, level, propagation)
        self._trace_ctx = TraceContext(self)

    @property
    def trace(self):
        return self._trace_ctx

    @staticmethod
    def _proper_extra(kwargs):
        return kwargs

    def enable_tracking(self, force_level=logging.DEBUG):
        TrackingLogger._is_tracking_enable = True
        self.force_level(force_level)

    def _flush_tracer(self, reset_level_before=False, reset_level_after=False):
        TrackingLogger._is_tracking_enable = False

        if reset_level_before:
            self.reset_level()

        logs = TrackingLogger._tracer.dump_logs()
        for log in logs:
            level, msg, args, kwargs = log
            self._log(level, msg, args, **kwargs)

        if reset_level_after:
            self.reset_level()

    def disable_tracking(self):
        self._flush_tracer(reset_level_before=True)

    def exit_with_exc(self):
        self._flush_tracer(reset_level_after=True)

    def _log(self, level, msg, args, **kwargs):
        kwargs = self._proper_extra(kwargs)
        if TrackingLogger._is_tracking_enable:
            TrackingLogger._tracer.log(level, msg, args, **kwargs)
        else:
            if self.isEnabledFor(level):
                PropagationLogger._log(self, level, msg, args, **kwargs)
