# coding:utf-8

from logging import Logger


class StructuredLogger(Logger):

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)
