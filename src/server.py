import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip = sys.argv[1]
port = int(sys.argv[2])

# Bind the socket to the port
server_address = (ip, port)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(64)
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data
    
    if data:
    	data += " " + `time.time()`
    	data += " " + `time.time()`
        sent = sock.sendto(data, address)
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)