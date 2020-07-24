from abc import ABC, abstractmethod
from typing import List, Any
import logging


class SourceChangeListener(ABC):

    @abstractmethod
    def source_changed(self, output_id, input_id):
        pass

    @abstractmethod
    def connected(self):
        pass

    @abstractmethod
    def disconnected(self):
        pass


class MultiplexingListener(SourceChangeListener):

    _listeners: List[SourceChangeListener]

    def __init__(self):
        self._listeners = []

    def source_changed(self, output_id, input_id):
        for listener in self._listeners:
            listener.source_changed(output_id, input_id)

    def connected(self):
        for listener in self._listeners:
            listener.connected()

    def disconnected(self):
        for listener in self._listeners:
            listener.disconnected()

    def register_listener(self, listener):
        self._listeners.append(listener)

    def unregister_listener(self, listener):
        self._listeners.remove(listener)


class LoggingListener(SourceChangeListener):

    def connected(self):
        logging.info(f"Connected")

    def disconnected(self):
        logging.info(f"Disconnected")

    def source_changed(self, output_id, input_id):
        logging.info(f"{output_id} changed to input: {input_id}")


class PrintingListener(SourceChangeListener):

    def connected(self):
        print("Connected")

    def disconnected(self):
        print("Disconnected")

    def source_changed(self, output_id, input_id):
        print(f"{output_id} changed to input: {input_id}")