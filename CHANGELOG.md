Change Log
=======================

v 0.18
------------

Make Hostname public

v 0.17
------------

Add an is_on method

v 0.16
------------

Bump aiohttp version

v 0.15
------------

Don't error if close() is called on a matrix that hasn't connected successfully.
Added mtrix metadata but you must use async_connect for this to be populated. 
Bumped aiohttp version


v0.11
------------

Add async_connect method

v0.10
------------

Fix missing version bump 

v0.9
------------

Fix url to github organisation


v0.8
------------

Move to github organisation

v0.7
------------

Don't error when a nonexistent listener is removed - log a warning instead.


v0.6
------------

Fix incorrect method name in TurningOnListener.

v0.5
------------

Extract the functionality "turn the matrix on when it is off and a change source is received." to a listener
so that it is easier to use.

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
