import optparse
import socket
import threading

hostName = '127.0.0.1'
portList = '21,25,80,110'
lock = threading.Semaphore(value = 1)

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
	resultString = ''
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	try:
		s.connect((resolvedHost, port))
		result = True
	except:
		result = False
	if result:
		# Port is open, try to get the banner
		try:
			s.send("Hello, world!\r\n")
			resultString = s.recv(100)
			resultString = resultString.split("\n", 2)[0].strip("\r")
		except:
			pass
	s.close()

	lock.acquire();
	if result:
		print "Port %5d/tcp is open. Response: '%s'" % (port, resultString)
	else:
		print "Port %5d/tcp is closed" % (port)
	lock.release()


def main():
	parseArguments()
	try:
		resolvedHost = socket.gethostbyname(hostName)
	except:
		print "Host cannot be resolved."
		exit(1)

	for port in portList.split(','):
		port = int(port.strip())
		thread = threading.Thread(target = checkPort, args = (resolvedHost, port))
		thread.start()


main()

