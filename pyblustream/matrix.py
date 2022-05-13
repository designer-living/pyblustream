from typing import Optional

from pyblustream.listener import MultiplexingListener
from pyblustream.protocol import MatrixProtocol


class Matrix:

    def __init__(self, hostname, port):
        self._multiplex_callback = MultiplexingListener()
        self._protocol = MatrixProtocol(hostname, port, self._multiplex_callback)

    def connect(self):
        self._protocol.connect()

    def close(self):
        self._protocol.close()

    def change_source(self, input_id: int, output_id: int):
        self._protocol.send_change_source(input_id, output_id)

    def update_status(self):
        self._protocol.send_status_message()

    def status_of_output(self, output_id: int) -> Optional[int]:
        return self._protocol.get_status_of_output(output_id)

    def status_of_all_outputs(self) -> list[tuple[int, Optional[int]]]:
        return self._protocol.get_status_of_all_outputs()

    def turn_on(self):
        self._protocol.send_turn_on_message()

    def turn_off(self):
        self._protocol.send_turn_off_message()

    def register_listener(self, listener):
        self._multiplex_callback.register_listener(listener)

    def unregister_listener(self, listener):
        self._multiplex_callback.unregister_listener(listener)
