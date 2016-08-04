import optparse
import socket


hostName = '127.0.0.1'
portList = '21,25,80,110'


def parseArguments():
	"""
	Parses arguments  on the command line.
	"""

	global hostName, portList

	parser = optparse.OptionParser("Usage: %prog hostname -p portlist\n\nPortlist is a comma-separated port list");
	parser.add_option('-p', dest = 'portList');
	(options, arguments) = parser.parse_args();

	if options.portList != None:
		portList = options.portList
	if len(arguments) > 0:
		hostName = arguments[0]

	return arguments


def checkPort(resolvedHost, port):
	"""
	Checks if the port is open
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	try:
		s.connect((resolvedHost, port))
		result = True
	except:
		result = False
	s.close

	return result


def main():
	parseArguments()
	try:
		resolvedHost = socket.gethostbyname(hostName)
	except:
		print "Host cannot be resolved."
		exit(1)

	for port in portList.split(','):
		port = int(port.strip())
		if checkPort(resolvedHost, port):
			print "Port %5d is open" % (port)
		else:
			print "Port %5d is closed" % (port)


main()

