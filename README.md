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
=====================================


    main.py -h <matrix ip address> [-p <port> -s <output_id> -o <output_id> -i <input_id> -a -l]
	    -h hostname or ip		Hostname or IP of the matrix - required
	    -p port			Port of the matrix to connect to - defaults to 23
	    -o output_id -i input_id	Set output ID to use input ID - specified as an int e.g. -i 2 -o 4 both must be specified
	    -s output_id	        Display the input for this output ID must be an int e.g. 2
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

See `example.py`
    
    
TODO
=======================

* Get names of inputs and outputs from the matrix
* Implement turn on / turn off
* Make the input for change_source and status_of_output to be consistent
    
Change Log
=======================

v0.4
------------

Implement Turn On/Turn Off for the matrix.

v0.3
------------

Ensure that we only use `int` for input and output ids

v0.2
------------

Upgrade to python 3.10

v0.1
------------

Initial Release