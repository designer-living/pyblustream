pyblustream
===========

pyblustream is a Python library to connect to an ELAN or Blustream HDBaseT Matrix. You can see the current mapping of inputs to outputs as well as 
request to change the input that an output is using.

It is primarily being developed with the intent of supporting [home-assistant](https://github.com/home-assistant/home-assistant)


Installation
------------

    # Installing from PyPI
    $ pip install pyblustream

Using on the command line as a script
===========================

    main.py -h <matrix ip address> [-p <port> -s <output_id> -o <output_id> -i <input_id> -a -l]
	    -h hostname or ip		Hostname or IP of the matrix - required
	    -p port			Port of the matrix to connect to - defaults to 23
	    -o output_id -i input_id	Set output ID to use input ID - specified as an int e.g. -i 2 -o 4 
	                                both must be specified
	    -s output_id	        Display the input for this output ID must be specified as a string zero starting e.g. 02
	    -a				Display the input for all outputs
	    -l				Continue running and listen for source changes

Log out the input used on a specific output and exit

    python3 main.py -h 127.0.0.1 -s 02

Log out all input/output mappings and exit

    python3 main.py -h 127.0.0.1 -a

Change display id 2 to source 3 and exit

    python3 main.py -h 127.0.0.1 -o 2 -i 3

Run forever logging status changes

    python3 main.py -h 127.0.0.1 -l

Change a source then run forever logging status changes

    python3 main.py -h 127.0.0.1 -o 2 -i 3 -l


Using in an application
=======================

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
    
    
TODO
=======================

* Get names of inputs and outputs from the matrix
* Implement turn on / turn off
* Make the input for change_source and status_of_output to be consistent
    