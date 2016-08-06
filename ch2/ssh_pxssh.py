import optparse
from pexpect import pxssh


def connect_ssh(host, user, password):
	"""
	Connects to ssh
	"""
	try:
		connection = pxssh.pxssh()
		connection.login(host, user, password)
	except Exception, e:
		print "Cannot establish connection: " + str(e)
		connection = None

	return connection


def send_command(connection, command):
	"""
	Sends a command to the connected ssh server
	"""
	connection.sendline(command)
	connection.prompt()

	return connection.before


def main():
	"""
	Establishes a connection and runs the command on the server
	"""
	parser = optparse.OptionParser(add_help_option = False, usage = 'Usage: %prog -h host -u username -p password')
	parser.add_option('-h', dest = 'host', help = 'Host to connect to')
	parser.add_option('-u', dest = 'user', help = 'User name to use')
	parser.add_option('-p', dest = 'password', help = 'Password to use')
	(options, args) = parser.parse_args()

	if options.host is None or options.user is None or options.password is None:
		parser.print_help()
		exit(1)

	connection = connect_ssh(options.host, options.user, options.password)
	if connection is None:
		exit(1)
	
	print send_command(connection, 'cat .profile')

	connection.logout()


main()

