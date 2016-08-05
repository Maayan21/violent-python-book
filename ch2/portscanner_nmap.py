import nmap
import optparse


hostName = '127.0.0.1'
ports = '10-465'


def parseArguments():
	"""
	Parses program arguments.
	"""
	global hostName, ports

	parser = optparse.OptionParser('Usage: %prog hostname [-p portrange]');
	parser.add_option('-p', dest = 'ports')
	(options, arguments) = parser.parse_args()

	if options.ports != None:
		ports = options.ports
	if len(arguments) > 0:
		hostName = arguments[0]


def printNmapResults(results):
	"""
	Prints nmap results.
	"""
	for host in results:
		result = results[host]
		if result['status']['state'] != 'up':
			print 'Host %s (%s) is down' % (result['hostnames'][0]['name'], host)
		else:
			print 'Host %s (%s) is up' % (result['hostnames'][0]['name'], host)
			for port in result['tcp']:
				portData = result['tcp'][port]
				if portData['name']:
					portName = ' (%s)' % (portData['name'])
				else:
					portName = ''
				info = 'Port %5d%s is %s' % (port, portName, portData['state'])
				print info


def runNmapScanner():
	"""
	Sets up and runs the scanner.
	"""
	scanner = nmap.PortScanner()
	try:
		result = scanner.scan(hostName, ports)
		if 'error' in result['nmap']['scaninfo']:
			for error in result['nmap']['scaninfo']['error']:
				print error
		else:
			printNmapResults(result['scan'])
	except Exception, e:
		print "Nmap output was not in the expected format: %s" % (e)


def main():
	"""
	Runs the scanner.
	"""
	parseArguments()
	runNmapScanner()

main()

