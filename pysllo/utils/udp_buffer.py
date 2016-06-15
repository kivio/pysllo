import socket
import sys


class UDPBuffer(object):
    def __init__(self, connections, limit=9000):
        self._connections = connections
        self._current = -1
        self.host, self.port = None, None
        self._round_connection()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._limit = limit

    def _round_connection(self):
        self._current = (self._current + 1) % len(self._connections)
        self.host, self.port = self._connections[self._current]

    def _send_msg(self, msg):
        self._socket.sendto(msg, (self.host, self.port))

    def send(self, msg):
        result = ''
        current_bytes = 0
        for data in msg:
            data_size = sys.getsizeof(data, 0)
            if data_size > self._limit:
                continue
            current_bytes += data_size
            if current_bytes <= self._limit:
                result += data
            else:
                self._send_msg(result)
                current_bytes = data_size
                result = data
        if current_bytes:
            self._send_msg(result)
        self._round_connection()
