import pytest


@pytest.fixture()
def socket():
    from tests.utils import TestSocket
    return TestSocket()


@pytest.fixture()
def buffer(socket):
    from pysllo.utils.udp_buffer import UDPBuffer

    udp = UDPBuffer([('localhost', 9700)])
    udp._socket = socket
    return udp


@pytest.fixture()
def buffer_with_rounding(socket):
    from pysllo.utils.udp_buffer import UDPBuffer

    udp = UDPBuffer([('localhost', 9700), ('localhost', 9701)])
    udp._socket = socket
    return udp


def test_simple_sending(socket, buffer):
    msg = "TEST"
    buffer.send(msg)
    data, (host, port) = socket.pop_with_connection()
    assert data == msg
    assert host == 'localhost'
    assert port == 9700


def test_too_long_message(socket, buffer):
    limit = 10
    buffer._limit = limit
    data = '123456789012345678901234567890'
    import sys
    assert sys.getsizeof(data, 0) > limit
    buffer.send([data])
    with pytest.raises(IndexError):
        socket.pop_with_connection()


def test_rounded_connection(socket, buffer_with_rounding):

    msg1 = "TEST1"
    msg2 = "TEST2"
    buffer_with_rounding.send(msg1)
    buffer_with_rounding.send(msg2)

    data_2, (host_2, port_2) = socket.pop_with_connection()
    data_1, (host_1, port_1) = socket.pop_with_connection()

    assert data_1 == msg1
    assert host_1 == 'localhost'
    assert port_1 == 9700

    assert data_2 == msg2
    assert host_2 == 'localhost'
    assert port_2 == 9701


def test_over_udp_limit(socket, buffer):
    msg1 = "TEST1"
    msg2 = "TEST2"

    import sys
    buffer._limit = sys.getsizeof(msg1) + 1

    buffer.send([msg1, msg2])
    data_2 = socket.pop_with_connection()[0]
    data_1 = socket.pop_with_connection()[0]

    assert data_1 == msg1
    assert data_2 == msg2
