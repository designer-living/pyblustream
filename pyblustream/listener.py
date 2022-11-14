from abc import ABC, abstractmethod
import time
from typing import List, Any
import logging


class SourceChangeListener(ABC):

    @abstractmethod
    def source_changed(self, output_id: int, input_id: int):
        pass

    @abstractmethod
    def connected(self):
        pass

    @abstractmethod
    def disconnected(self):
        pass

    @abstractmethod
    def power_changed(self, power: bool):
        pass

    def error(self, error_message: str):
        # By default, do nothing but can be overwritten to be notified of these messages.
        pass

    def source_change_requested(self, output_id: int, input_id: int):
        # By default, do nothing but can be overwritten to be notified of these messages.
        pass


class MultiplexingListener(SourceChangeListener):

    _listeners: List[SourceChangeListener]

    def __init__(self):
        self._listeners = []

    def source_changed(self, output_id: int, input_id: int):
        for listener in self._listeners:
            listener.source_changed(output_id, input_id)

    def power_changed(self, power: bool):
        for listener in self._listeners:
            listener.power_changed(power)

    def connected(self):
        for listener in self._listeners:
            listener.connected()

    def disconnected(self):
        for listener in self._listeners:
            listener.disconnected()

    def error(self, error_message: str):
        for listener in self._listeners:
            listener.error(error_message)

    def source_change_requested(self, output_id: int, input_id: int):
        for listener in self._listeners:
            listener.source_change_requested(output_id, input_id)

    def register_listener(self, listener: SourceChangeListener):
        self._listeners.append(listener)

    def unregister_listener(self, listener: SourceChangeListener):
        self._listeners.remove(listener)


class LoggingListener(SourceChangeListener):

    def connected(self):
        logging.info(f"Connected")

    def disconnected(self):
        logging.info(f"Disconnected")

    def source_changed(self, output_id: int, input_id: int):
        logging.info(f"{output_id} changed to input: {input_id}")

    def power_changed(self, power: bool):
        logging.info(f"Power changed to : {power}")


class PrintingListener(SourceChangeListener):

    def connected(self):
        print("Connected")

    def disconnected(self):
        print("Disconnected")

    def source_changed(self, output_id, input_id):
        print(f"{output_id} changed to input: {input_id}")

    def power_changed(self, power: bool):
        print(f"Power changed to : {power}")


class TurningOnListener(SourceChangeListener):

    TIMEOUT_SECONDS = 15

    def __init__(self, matrix):
        self.last_requested_output_id = None
        self.last_requested_input_id = None
        self.last_requested_at = 0
        self.change_source_on_power_on = False
        self.matrix = matrix

    def source_changed(self, output_id: int, input_id: int):
        pass

    def connected(self):
        pass

    def disconnected(self):
        pass

    def power_changed(self, power: bool):
        if self.change_source_on_power_on and power:
            self.change_source_on_power_on = False
            print(
                f"Attempting to change matrix source output "
                f"{self.last_requested_output_id} to input {self.last_requested_input_id}"
            )
            self.matrix.change_source(int(self.last_requested_input_id), int(self.last_requested_output_id))
            self.last_requested_output_id = None
            self.last_requested_input_id = None

    def error(self, error_message: str):
        error_at = time.time()
        if self.last_requested_at > (error_at - self.TIMEOUT_SECONDS) and\
                self.last_requested_input_id is not None and\
                self.last_requested_output_id is not None:
            self.last_requested_at = 0
            print(f"Attempting to turn on matrix")
            self.matrix.turn_on()
            self.change_source_on_power_on = True
            # We will change the source once we get a successful matrix turned on event.

    def source_change_requested(self, output_id: int, input_id: int):
        self.last_requested_output_id = output_id
        self.last_requested_input_id = input_id
        self.last_requested_at = time.time()
