from abc import ABC, abstractmethod
import time
from typing import List
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
        if listener in self._listeners:
            self._listeners.remove(listener)
        else:
            logging.info("Listener isn't registered")


class LoggingListener(SourceChangeListener):

    def __init__(self, logger = logging):
        self.logger = logger

    def connected(self):
        self.logger.info("Connected")

    def disconnected(self):
        self.logger.info("Disconnected")

    def source_changed(self, output_id: int, input_id: int):
        self.logger.info(f"{output_id} changed to input: {input_id}")

    def power_changed(self, power: bool):
        self.logger.info(f"Power changed to : {power}")


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
    """
    Listener that will turn on the Matrix if a user makes a chnage using the matrix mobile app.
    The standard behaviour for the mobile app is to ignore source changes if the matrix is turned off.
    """

    TIMEOUT_SECONDS = 15

    def __init__(self, matrix, logger = logging):
        self.last_requested_output_id = None
        self.last_requested_input_id = None
        self.last_requested_at = 0
        self.change_source_on_power_on = False
        self.matrix = matrix
        self.logger = logger

    def source_changed(self, output_id: int, input_id: int):
        pass

    def connected(self):
        pass

    def disconnected(self):
        pass

    def power_changed(self, power: bool):
        if self.change_source_on_power_on and power:
            self.change_source_on_power_on = False
            self.logger.info(
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
            self.logger.info("Attempting to turn on matrix")
            self.matrix.turn_on()
            self.change_source_on_power_on = True
            # We will change the source once we get a successful matrix turned on event.

    def source_change_requested(self, output_id: int, input_id: int):
        self.last_requested_output_id = output_id
        self.last_requested_input_id = input_id
        self.last_requested_at = time.time()
