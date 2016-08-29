import dpkt
import socket
import sys

if len(sys.argv) != 2:
	print "Usage: print_pcap.py file.pcap"
	exit(1)

pcapFile = None
try:
	pcapFile = open(sys.argv[1], 'rb')
	reader = dpkt.pcap.Reader(pcapFile)
except:
	if pcapFile is not None:
		close(pcapFile)
	print "Unable to open %s" % (sys.argv[1])
	exit(1)

nsCache = {}
for (ts, buffer) in reader:
	try:
		ethPacket = dpkt.ethernet.Ethernet(buffer)
		ipAddresses = ethPacket.data
		sourceIpAddress = socket.inet_ntoa(ipAddresses.src)
		destinationIpAddress = socket.inet_ntoa(ipAddresses.dst)
		if destinationIpAddress not in nsCache:
			try:
				nsCache[destinationIpAddress] = socket.gethostbyaddr(destinationIpAddress)[0]
			except:
				nsCache[destinationIpAddress] = '?'
		print "%s -> %s (%s)" % (sourceIpAddress, destinationIpAddress, nsCache[destinationIpAddress])
	except:
		print "Malformed packet?"

pcapFile.close()

