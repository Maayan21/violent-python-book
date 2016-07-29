from passlib.context import CryptContext

def testpass(password, dictionary):
	context = CryptContext(schemes = ['des_crypt', 'md5_crypt', 'sha256_crypt', 'sha512_crypt'])
	for word in dictionary:
		try:
			if context.verify(word, password):
				return word
		except ValueError, e:
			pass
	return None

def main():
	dictionaryFile = open('dictionary.txt', 'r')
	dictionary = [x.strip() for x in dictionaryFile.readlines()]
	dictionaryFile.close();
	passwordFile = open('shadow', 'r')
	for line in passwordFile:
		lineParts = [x.strip() for x in line.split(':')]
		foundPassword = testpass(lineParts[1], dictionary)
		if foundPassword != None:
			print "Password for user %s is %s" % (lineParts[0], foundPassword)
		else:
			print "Password was not found for user %s" % (lineParts[0])
	passwordFile.close()

main()

