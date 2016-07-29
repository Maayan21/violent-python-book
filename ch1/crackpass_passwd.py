import crypt

def testpass(password, dictionary):
	salt = password[0:2]
	for word in dictionary:
		if crypt.crypt(word, salt) == password:
			return word
	return None

def main():
	dictionaryFile = open('dictionary.txt', 'r')
	dictionary = [x.strip() for x in dictionaryFile.readlines()]
	dictionaryFile.close();
	passwordFile = open('passwd', 'r')
	for line in passwordFile:
		lineParts = [x.strip() for x in line.split(':')]
		foundPassword = testpass(lineParts[1], dictionary)
		if foundPassword != None:
			print "Password for user %s is %s" % (lineParts[0], foundPassword)
		else:
			print "Password was not found for user %s" % (lineParts[0])
	passwordFile.close()

main()

