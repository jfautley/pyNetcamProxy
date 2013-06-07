pyNetcamProxy
=============

Python tool to proxy MJPEG Network Camera streams to multiple clients.

Currently the code is just a proof of concept of Python processing a
multipart/x-mixed-replace stream and dumping to individual files.

Eventually, we should provide a threaded HTTP server permitting multiple
client connections, and serving up the MJPEG stream as proxied and
possibly processed from the source camera. Connection to the source
camera should be closed if there are no active client connections.
