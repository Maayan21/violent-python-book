import dpkt
import pygeoip
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

try:
	geoIp = pygeoip.GeoIP('/opt/local/share/GeoIP/GeoLiteCity.dat')
except:
	print 'Cannot open GeoIP database'
	exit(1)

nsCache = {}
geoCache = {}
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
		if destinationIpAddress not in geoCache:
			try:
				record = geoIp.record_by_name(destinationIpAddress)
				geoInfo = ''
				print str(record)
				if record['city'] != '':
					geoInfo = record['city']
				if record['country_code3']:
					if geoInfo != '':
						geoInfo = geoInfo + ', '
					geoInfo = geoInfo + record['country_code3']
				if record['longitude'] is not None and record['latitude'] is not None:
					if geoInfo != '':
						geoInfo = geoInfo + ', '
					geoInfo = geoInfo + str(record['longitude']) + ', ' + str(record['latitude'])
				if geoInfo == '':
					geoInfo = 'no geo info'
				geoCache[destinationIpAddress] = '(' + geoInfo + ')'
			except Exception, e:
				print str(e)
				geoCache[destinationIpAddress] = '(cannot resolve)'
		print "%s -> %s (%s; %s)" % (sourceIpAddress, destinationIpAddress, geoCache[destinationIpAddress], nsCache[destinationIpAddress])
	except:
		print "Malformed packet?"

pcapFile.close()

