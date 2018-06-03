import sys

path = sys.argv[1]

with open(path) as file:
	lines = file.readlines()
lines = [line.strip() for line in lines]

rtt_sum = 0.0
offset_sum = 0.0
count=0
current_id=0
list = list()

for line in lines:
	split=line.split(";")
	result = split[0]
	if result=="SUCCESS":
		count+=1
		
		current_id=int(split[1].split()[0])
		rtt_offset=split[2].split(",")
		rtt=float(rtt_offset[0])
		offset=float(rtt_offset[1])

		#instantaneous number for histogram
		#take avg of previous till now
		if count>1 :
			prev_avg = offset_sum/(count-1);
			instantaneous_avg = (prev_avg + offset)/2
			list.append(instantaneous_avg)
		#add for average
		rtt_sum += rtt
		offset_sum += offset

#calculate the average
rtt_avg = rtt_sum/count #round trip average
offset_avg = offset_sum/count #offset average

print >>sys.stderr, "Current_id: %d " % current_id
print >>sys.stderr, "Count: %d " % count

packetloss_rate = ((current_id-count)/current_id) * 100 #

file = open("report_info.txt","a")

file.write("RTT average: " + `rtt_avg`)
file.write("\n")
file.write("Offset average: " + `offset_avg`)
file.write("\n")
file.write("Avg drift time: " + `1-offset_avg`)
file.write("\n")
file.write("Packet loss rate: " + `packetloss_rate`)
file.write("\n")

print >>sys.stderr, "RTT average: %f " % rtt_avg
print >>sys.stderr, "Offset average: %f " % offset_avg
print >>sys.stderr, "Packet loss rate: %f " % packetloss_rate

file.write("Instantaneous Offset Values: \n")
for value in list:

	file.write(`value`+"\n")

