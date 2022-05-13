import asyncio
import logging
import re
from asyncio import Task
from typing import Any, Optional

from pyblustream.listener import SourceChangeListener

SUCCESS_CHANGE = re.compile('.*SUCCESS.*output\\s*([0-9]+)\\sconnect from input\\s*([0-9]+).*')
OUTPUT_CHANGE = re.compile('.*OUT\\s*([0-9]+)\\s*FR\\s*([0-9]+).*', re.IGNORECASE)
STATUS_LINE = re.compile('([0-9][0-9])\\s+([0-9][0-9])[^:].*')


class MatrixProtocol(asyncio.Protocol):

    _received_message: str
    _heartbeat_task: Optional[Task[Any]]
    _connected: bool
    _output_to_input_map: dict[int, int]
    _source_change_callback: SourceChangeListener

    def __init__(self, hostname, port, callback: SourceChangeListener, heartbeat_time=5, reconnect_time=10):
        self._logger = logging.getLogger(__name__)
        self._heartbeat_time = heartbeat_time
        self._reconnect_time = reconnect_time
        self._hostname = hostname
        self._port = port
        self._source_change_callback = callback
        self._loop = asyncio.get_event_loop()

        self._connected = False
        self._reconnect = True
        self._transport = None
        self.peer_name = None
        self._received_message = ""
        self._output_to_input_map = {}
        self._heartbeat_task = None

    def connect(self):
        connection_task = self._loop.create_connection(lambda: self, host=self._hostname, port=self._port)
        self._loop.create_task(connection_task)

    def close(self):
        self._reconnect = False
        self._transport.close()

    def connection_made(self, transport):
        self._connected = True
        self._transport = transport
        self.peer_name = transport.get_extra_info("peername")
        self._logger.info(f"Connection Made: {self.peer_name}")
        self._logger.info("Requesting current status")
        self._source_change_callback.connected()
        self.send_status_message()
        self._heartbeat_task = self._loop.create_task(self._heartbeat())

    async def _heartbeat(self):
        while True:
            await asyncio.sleep(self._heartbeat_time)
            self._logger.debug('heartbeat')
            self._data_send("\n")

    async def wait_to_reconnect(self):
        while not self._connected and self._reconnect:
            await asyncio.sleep(self._reconnect_time)
            self.connect()

    def connection_lost(self, exc):
        self._connected = False
        self._heartbeat_task.cancel()
        disconnected_message = f"Disconnected from {self._hostname}"
        if self._reconnect:
            disconnected_message = disconnected_message + " will try to reconnect in {self._reconnect_time} seconds"
            self._logger.error(disconnected_message)
        else:
            disconnected_message = disconnected_message + " not reconnecting"
            # Only info in here as close has been called.
            self._logger.info(disconnected_message)
        self._source_change_callback.disconnected()
        if self._reconnect:
            self._loop.create_task(self.wait_to_reconnect())
        pass

    def data_received(self, data):
        self._logger.debug(f"data_received client: {data}")

        for letter in data:
            # Don't add these to the message as we don't need them.
            if letter != ord('\r') and letter != ord('\n'):
                self._received_message += chr(letter)
            if letter == ord('\n'):
                self._logger.debug(f"Whole message: {self._received_message}")
                self._process_received_packet(self._received_message)
                self._received_message = ''

    def _data_send(self, message):
        self._logger.debug(f"data_send client: {message.encode()}")
        self._transport.write(message.encode())

    def _process_received_packet(self, message):
        match = SUCCESS_CHANGE.match(message)
        if match:
            self._logger.debug(f"Input change message received: {message}")
            output_id = match.group(1)
            input_id = match.group(2)
            self._process_input_changed(input_id, output_id)
        else:
            match = STATUS_LINE.match(message)
            if match:
                self._logger.debug(f"Status Input change message received: {message}")
                output_id = match.group(1)
                input_id = match.group(2)
                self._process_input_changed(input_id, output_id)
            else:
                self._logger.debug(f"Not an input change message received: {message}")

    def _process_input_changed(self, input_id, output_id):
        self._logger.debug(f"Input ID [{input_id}] Output id [{output_id}]")
        input_id_int = int(input_id)
        output_id_int = int(output_id)
        self._output_to_input_map[output_id_int] = input_id_int
        self._source_change_callback.source_changed(output_id_int, input_id_int)

    def send_change_source(self, input_id: int, output_id: int):
        self._logger.info(f"Sending Output source change message - Output: {output_id} changed to input: {input_id}")
        self._data_send(f"out{output_id:02d}fr{input_id:02d}\r")

    def send_status_message(self):
        self._logger.info(f"Sending status change message")
        self._data_send("STATUS\r")

    def get_status_of_output(self, output_id: int) -> Optional[int]:
        return self._output_to_input_map.get(output_id, None)

    def get_status_of_all_outputs(self) -> list[tuple[int, Optional[int]]]:
        return_list: list[tuple[int, int | None]] = []
        for output_id in self._output_to_input_map:
            input_id = self._output_to_input_map.get(output_id, None)
            return_list.append((output_id, input_id))
        return return_list

    def send_turn_on_message(self):
        pass

    def send_turn_off_message(self):
        pass
