from typing import Optional

from pyblustream.listener import MultiplexingListener
from pyblustream.protocol.telent import MatrixTelnetProtocol
from pyblustream.protocol.http import MatrixHttpProtocol


class Matrix:

    def __init__(self, hostname, port):
        self._multiplex_callback = MultiplexingListener()
        self._telnet_protocol = MatrixTelnetProtocol(hostname, port, self._multiplex_callback)
        self._http_protocol = MatrixHttpProtocol(hostname, self._multiplex_callback)

    def connect(self):
        self._http_protocol.connect()
        self._telnet_protocol.connect()

    def close(self):
        self._http_protocol.close()
        self._telnet_protocol.close()

    def change_source(self, input_id: int, output_id: int):
        self._telnet_protocol.send_change_source(input_id, output_id)

    def update_status(self):
        self._telnet_protocol.send_status_message()

    def status_of_output(self, output_id: int) -> Optional[int]:
        return self._telnet_protocol.get_status_of_output(output_id)

    def status_of_all_outputs(self) -> list[tuple[int, Optional[int]]]:
        return self._telnet_protocol.get_status_of_all_outputs()

    def turn_on(self):
        self._telnet_protocol.send_turn_on_message()

    def turn_off(self):
        self._telnet_protocol.send_turn_off_message()

    def register_listener(self, listener):
        self._multiplex_callback.register_listener(listener)

    def unregister_listener(self, listener):
        self._multiplex_callback.unregister_listener(listener)
