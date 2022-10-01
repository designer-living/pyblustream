import asyncio
import logging
import re
import time
from asyncio import Task
from typing import Any, Optional

from pyblustream.listener import SourceChangeListener

# Success message after output has changed:
# [SUCCESS]Set output 05 connect from input 03.
SUCCESS_CHANGE = re.compile(r'.*SUCCESS.*output\s*(\d+)\sconnect from input\s*(\d+).*')
# Success System powered off:
# [SUCCESS]Set system power OFF
# Success system powered on:
# [SUCCESS]Set system power ON, please wait a moment... Done
SUCCESS_POWER = re.compile(r'.*SUCCESS.*Set system power\s*(\w+).*')

# Sent from app comes like this:
# EL-4KPM-V88> out06fr02
# OUTPUT_CHANGE = re.compile('.*(?:OUT|out)\\s*([0-9]+)\\s*(?:FR|fr)\\s*([0-9]+).*', re.IGNORECASE)
OUTPUT_CHANGE = re.compile(r'.*OUT\s*(\d+)\s*FR\s*(\d+).*', re.IGNORECASE)

# The line in a status message that shows the input/output status:
# '01	     01		  No /Yes	  Yes/SRC   	HDBT      ON '
INPUT_STATUS_LINE = re.compile(r'(\d\d)\s+(\d\d)[^:].*')
# The line in a status message that shows the  system power status:
# Power	IR	Key	Beep	LCD
# ON 	ON 	ON 	OFF	ON
FIRST_LINE = re.compile(r'.*Power\s+IR\s+Key\s+Beep\s+LCD.*')
POWER_STATUS_LINE = re.compile(r'.*(ON|OFF)\s+(ON|OFF)\s+(ON|OFF)\s+(ON|OFF)\s+(ON|OFF).*')

# Received if you try to change inputs using the app when the matrix is OFF:
# From the app: out04fr08
# [ERROR]System is power off, please turn it on first.
ERROR_OFF = re.compile(r'.*ERROR.*System is power off, please turn it on first.*')

TIMEOUT_SECONDS = 15

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
        self._matrix_on = False
        self._heartbeat_task = None

        # This is a nice to have - if someone tries to change the matrix source (e.g. using the phone app)
        # We will spot the matrix isn't on - turn it on for them and then re-send the change source message.
        self.last_output_id = None
        self.last_input_id = None
        self.last_set_at = 0
        self.change_source_on_power_on = False

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

        # Message received in response to anyone changing the source.
        success_change_match = SUCCESS_CHANGE.match(message)
        if success_change_match:
            self._logger.debug(f"Input change message received: {message}")
            output_id = success_change_match.group(1)
            input_id = success_change_match.group(2)
            self._process_input_changed(input_id, output_id)
            return

        # Message received in response to anyone changing the power on/off
        success_power_match = SUCCESS_POWER.match(message)
        if success_power_match:
            self._logger.debug(f"Power change message received: {message}")
            power = success_power_match.group(1)
            self._process_power_changed(power)
            if self.change_source_on_power_on:
                self.change_source_on_power_on = False
                self._logger.info(
                    f"Attempting to change matrix source output {self.last_output_id} to input {self.last_input_id}")
                self.send_change_source(int(self.last_input_id), int(self.last_output_id))
                self.last_output_id = None
                self.last_input_id = None

            return

        # Someone has sent a message to change the source
        output_change_match = OUTPUT_CHANGE.match(message)
        if output_change_match:
            self._logger.debug(f"Input change message received: {message}")
            self.last_output_id = output_change_match.group(1)
            self.last_input_id = output_change_match.group(2)
            self.last_set_at = time.time()
            return

        error_match = ERROR_OFF.match(message)
        if error_match:
            self._logger.info(f"Error message received: {message}")
            error_at = time.time()
            if self.last_set_at > (error_at - TIMEOUT_SECONDS) and\
                    self.last_input_id is not None and\
                    self.last_output_id is not None:
                self.last_set_at = 0
                self._logger.info(f"Attempting to turn on matrix")
                self.send_turn_on_message()
                self.change_source_on_power_on = True
                # We will change the source once we get a successful matrix turned on event.
            return

        # Lines that show inputs/outputs when someone has called STATUS
        input_status_change_match = INPUT_STATUS_LINE.match(message)
        if input_status_change_match:
            self._logger.debug(f"Status Input change message received: {message}")
            output_id = input_status_change_match.group(1)
            input_id = input_status_change_match.group(2)
            self._process_input_changed(input_id, output_id)
            return

        # Lines that show inputs/outputs when someone has called STATUS
        power_status_change_match = POWER_STATUS_LINE.match(message)
        if power_status_change_match:
            self._logger.debug(f"Status Power message received: {message}")
            power = power_status_change_match.group(1)
            self._process_power_changed(power)
            return

        self._logger.debug(f"Not an input change message received: {message}")

    def _process_input_changed(self, input_id, output_id):
        self._logger.debug(f"Input ID [{input_id}] Output id [{output_id}]")
        input_id_int = int(input_id)
        output_id_int = int(output_id)
        self._output_to_input_map[output_id_int] = input_id_int
        self._source_change_callback.source_changed(output_id_int, input_id_int)

    def _process_power_changed(self, power):
        self._logger.debug(f"Power change to [{power}]")
        self._matrix_on = power == "ON"  # Otherwise it is OFF
        self._source_change_callback.power_changed(power)

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

    def is_matrix_on(self) -> bool:
        return self._matrix_on

    def send_turn_on_message(self):
        self._data_send(f"PON\r")

    def send_turn_off_message(self):
        self._data_send(f"POFF\r")
