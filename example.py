import asyncio
import logging

from pyblustream.listener import SourceChangeListener
from pyblustream.matrix import Matrix


class MyListener(SourceChangeListener):

    def __init__(self, connected_event: asyncio.Event = None):
        self._connected_event = connected_event

    def source_changed(self, output_id, input_id):
        # Your code to run when the source changes
        print("Source Changed Output ", output_id, " input ", input_id)
        pass

    def connected(self):
        # Your code to run on a successful connection to the matrix
        # For now we set event to say the matrix is connected
        if self._connected_event is not None:
            self._connected_event.set()
        print("Connected")

    def disconnected(self):
        # Your code to run when disconnected from the matrix
        # Note: the library will try to reconnect, so you don't need to
        print("Disconnected")


async def stop_in(seconds, event: asyncio.Event):
    await asyncio.sleep(seconds)
    event.set()


async def main():
    # Set to your details
    ip = "192.168.1.160"
    port = 23
    # Create a matrix
    matrix = Matrix(ip, port)
    # Register a listener so you can handle state changes
    connected_event = asyncio.Event()
    matrix.register_listener(MyListener(connected_event))
    # You always need to connect to the matrix - best to do this after
    # adding your listener to avoid missing the initial status that is returned on start up
    matrix.connect()
    await connected_event.wait()

    await asyncio.sleep(2)

    # Programmatically change the source for output 2 to input 3.
    matrix.change_source(3, 5)

    print("--- All Outputs --- ")
    all_outputs = matrix.status_of_all_outputs()
    print(all_outputs)
    print("--- Input for Zone 1 --- ")
    input_for_zone_one = matrix.status_of_output(1)
    print(input_for_zone_one)

    # Force the matrix to refresh its status
    # This is done automatically on startup/reconnect, so you shouldn't need to do this
    matrix.update_status()

    await asyncio.sleep(1)
    matrix.close()
    await asyncio.sleep(1)

    print("Done")

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    asyncio.run(main())
