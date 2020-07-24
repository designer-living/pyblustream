import asyncio

from pyblustream.listener import SourceChangeListener
from pyblustream.matrix import Matrix


class MyListener(SourceChangeListener):

    def source_changed(self, output_id, input_id):
        # Your code to run when the source changes
        pass

    def connected(self):
        # Your code to run on a successful connection to the matrix
        pass

    def disconnected(self):
        # Your code to run when disconnected from the matrix
        # Note: the library will try to reconnect so you don't need to
        pass


# Set to your details
ip = "127.0.0.1"
port = 23
# Use an asyncio event loop - you will need to make sure this runs
my_loop = asyncio.get_event_loop()
# Create a matrix
matrix = Matrix(ip, port, loop=my_loop)
# Register a listenerer so you can handle state changes
matrix.register_listener(MyListener())
# You always need to connect to the matrix - best to do this after
# adding your listener to avoid missing the inital status that is returned on start up
matrix.connect()

# Programmatically change the source for output 2 to input 3.
matrix.change_source(2, 3)

all_outputs = matrix.status_of_all_outputs()
input_for_zone_one = matrix.status_of_output("01")
# Force the matrix to refresh it's status
# This is done automatically on startup/reconnect so you shouldn't need to do this
matrix.update_status()
my_loop.run_forever()
