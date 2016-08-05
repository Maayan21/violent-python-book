import os
import sys
import tempfile
import zipfile


def getTempDir():
	"""
	Returns the temporarary directory path (or the current path if the system has no temporary directory).
	"""
	tempDir = tempfile.gettempdir()
	if tempDir == None:
		tempDir = os.getcwd()

	return tempDir


def findSmallestFileInZip(zipFile):
	"""
	Finds the smallest file in the zip file.

	zipFile: zipfile.ZipFile
	"""
	foundSize = -1
	fileName = None
	for zipInfo in zipFile.infolist():
		if zipInfo.file_size < foundSize or foundSize < 0:
			foundSize = zipInfo.file_size
			fileName = zipInfo.filename

	return fileName


def checkIfZipHasPassword(zipFile, smallestFile):
	"""
	Checks if the zipFile has a password.

	zipFile: zipfile.ZipFile
	smallestFile: string - name of the file in the archive
	"""
	try:
		tempDir = getTempDir()
		realPath = zipFile.extract(smallestFile, tempDir)
		result = False
		try:
			# Clean up
			os.unlink(realPath)
			dirSegments = realPath.split(os.sep, 2);
			if len(dirSegments) > 1:
				os.removedirs(tempDir + os.sep + dirSegments[0]);
		except:
			# Can't do anything here...
			pass
	except:
		# Seems to have the password
		result = True

	return result


def crackZipPassword(zipFileName, dictionaryFileName):
	"""
	Executes a dictionary attack on the zip file. Parameters are self-explanatory.
	"""
	zipFile = zipfile.ZipFile(zipFileName, 'r');
	smallestFile = findSmallestFileInZip(zipFile)

	if smallestFile == None:
		print "Zip archive is empty"
		return

	if not checkIfZipHasPassword(zipFile, smallestFile):
		print "Zip file does not have password protection"
		return

	dictionaryFile = open(dictionaryFileName, 'r');
	tempDir = getTempDir()
	foundPassword = None
	for password in dictionaryFile:
		try:
			password = password.rstrip("\r\n");
			zipFile.extract(smallestFile, tempDir, password)
			foundPassword = password
			break
		except:
			# Bad password
			pass
	dictionaryFile.close()
	if foundPassword == None:
		print "Password is not in the dictionary"
	else:
		print "Found password: '%s'" % (password)


def main():
	"""
	Runs the cracker.
	"""
	if len(sys.argv) != 3:
		print "Format: python crackzip.py filename.zip dictionary.txt"
	else:
		fileName = sys.argv[1]
		dictionary = sys.argv[2]
		if os.path.exists(fileName) and os.path.isfile(fileName):
			if os.path.exists(dictionary) and os.path.isfile(dictionary):
				crackZipPassword(fileName, dictionary)
			else:
				print "Dictionary file '%s' does not exist" % (dictionary)
		else:
			print "File '%s' does not exist" % (fileName)

main()

