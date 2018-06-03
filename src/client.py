import socket
import sys
import time

# Method to fetch estimate with lowest RTT from the list
def getLowestRtt(list):
	if len(list)==0:
		return "0;0"
	estimate_low = list[0]
	rtt_,offset_ = estimate_low.split(";")
	rtt_low = float(rtt_)
	offset_low = float(offset_)

	for estimate in list:
		rtt,offset = estimate.split(";")
		rtt_num = float(rtt)
		offset_num = float(offset)
		if rtt_num < rtt_low:
			estimate_low = estimate
			rtt_low = rtt_num

	return estimate_low

ip = sys.argv[1]
server_port = int(sys.argv[2])

file = open("log" + `time.time()` + ".txt", "a");
server_address = (ip, server_port)
list = list()
id = 1
data = ""
while True:
	starttime = time.time()
	# Create a UDP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(1);
	message = ''
	message+= `id` + " " + `time.time()`

	try:
		# Send data
		print >>sys.stderr, 'sending "%s"' % message
		sent = sock.sendto(message, server_address)
		# Receive response
		print >>sys.stderr, 'waiting to receive'
		data, server = sock.recvfrom(64)
		print >>sys.stderr, 'received "%s"' % data
		data += " " + `time.time()`
		print >>sys.stderr, 'final "%s"' % data
		# Interaction Successful, get lowest recent estimate.
		estimate_low = getLowestRtt(list)
		smoothening = float(estimate_low.split(";")[1])
		correctedTime = time.time() + smoothening
		print >>sys.stderr, "correctedTime: %f" %correctedTime 
		print >>sys.stderr, "LowestEstimate: %s" % estimate_low
		# Calculate RTT and Drift
		seq_s,t3_s,t2_s,t1_s,t0_s = data.split(" ")
		t3 = float(t3_s)
		t2 = float(t2_s)
		t1 = float(t1_s)
		t0 = float(t0_s)

		print >>sys.stderr, "t3: %f " % t3
		print >>sys.stderr, "t2: %f " % t2
		print >>sys.stderr, "t1: %f " % t1
		print >>sys.stderr, "t0: %f " % t0

		rtt = (t2-t3) + (t0-t1)
		offset = ((t2-t3)-(t0-t1))/2
		# LOG the information.
		# ALSO, log client hardware clock time + smoothening offset as well.
		file.write("SUCCESS" + ";" + data + ";" 
			+ "("+ `rtt` +","+`offset` + ")" + ";" + `correctedTime`)
		file.write("\n")
		# Add to queue. To maintain last 8. 
		if len(list)==8 :
			list = list[1:]
		list.append(`rtt` +";"+ `offset`)	
		print >>sys.stderr, "rtt: %f" % rtt
		print >>sys.stderr, "offset: %f" % offset
	except socket.timeout:
		print >>sys.stderr, 'Timeout'
		file.write("FAILURE;"+message)


	print >>sys.stderr, "\n"
	id = id + 1
	time.sleep(10 - (time.time()-starttime))    
