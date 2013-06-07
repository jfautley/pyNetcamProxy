#!/usr/bin/python

""" Webcam Proxy """

import requests
import sys
import time

req = requests.get('http://hostname/videostream.cgi', auth=('user', 'password'), stream=True)

print req.headers

# Get our boundary marker
if req.headers['content-type'].startswith('multipart/'):
    print "Got a multipart stream!"
    boundary = req.headers['content-type'].rsplit(';boundary=')[1]
    print "[%s]" % boundary
else:
    print "Looks like we're not being fed multipart data?"
    sys.exit(1)
while True:
    # Snarf the beginning of the request, to find our headers
    chunk = req.raw.read(1024)
    chunk_split = chunk.split("\r\n\r\n", 1)
    for head in chunk_split[0].splitlines():
        if head.startswith("Content-Length:"):
            clen = head.split(": ", 1)[1]
            print "Content len is %d" % int(clen)
    
    print "%d bytes remaining..." % len(chunk_split[1])
    remaining = int(clen) - len(chunk_split[1])
    print "Need to read %d bytes more" % remaining
    
    img = chunk_split[1] + req.raw.read(remaining)
    print "Image is %d bytes long" % len(img)
    
    f = open('img-%s.jpg' % time.time(), 'wb')
    f.write(img)
    f.close()
    
sys.exit(0)


for chunk in req.raw.read(512):
    # split our chunk
    chunk_split = chunk.strip().split("--%s\r\n" % boundary)

    if len(chunk_split) > 1:
        # We've found a header...
        header = chunk_split[1].strip().split('\r\n\r\n', 1)
        print header[0]
