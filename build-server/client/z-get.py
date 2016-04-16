#!/usr/bin/env python
import socket
import sys


remoteIP, str_PORT = socket.gethostbyname('10.239.131.30'), '16180'
data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(('127.0.0.1', int(str_PORT)))
    sock.sendall(str(sys.argv[1:]))
    received = sock.recv(1 << 20)
finally:
    sock.close

print "Sent:\n%s" % (data)
print "Received:\n%s" % (received)
exec received
