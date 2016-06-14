import logging

from pysllo.utils.tracer import Tracer


def test_simple_tracing():
    msg = 'TEST'
    tracer = Tracer()
    tracer.log(logging.INFO, msg)
    logs = tracer.dump_logs()
    assert len(logs) == 1
    log = logs[0]
    assert log[0] == logging.INFO
    assert log[1] == msg
