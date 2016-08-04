import os
import sys
import tempfile
import zipfile


def getTempDir():
	tempDir = tempfile.gettempdir()
	if tempDir == None:
		tempDir = os.getcwd()

	return tempDir

def findSmallestFileInZip(zipFile):
	foundSize = -1
	fileName = None
	for zipInfo in zipFile.infolist():
		if zipInfo.fileSize < foundSize or foundSize < 0:
			foundSize = zipInfo.filename

	return fileName


def checkIfZipHasPassword(zipFile, smallestFile):
	try:
		tempDir = getTempDir()
		realPath = zipFile.extract(smallestFile, tempDir)
		try:
			# Clean up
			os.unlink(realPath)
			dirSegments = realPath.split(os.sep, 2);
			if len(dirSegments) > 1:
				os.removedirs(tempDir + os.sep + dirSegments[0]);
		except:
			# Can't do anything here...
			pass
		print "Zip file does not have password protection\n"
		exit(1)
	except:
		# Seems to have the password
		pass

def crackZipPassword(zipFileName, dictionaryFileName):
	zipFile = zipfile.ZipFile(zipFIleName, 'r');
	smallestFile = findSmallestFileInZip(zipFile)
	if smallestFile == None:
		print "Zip archive is empty\n"
		exit(1)
	checkIfZipHasPassword(zipFile, smallestFile)
	dictoinaryFile = open(dictionaryFileName, 'r');
	for password in dictionaryFile:
		# TODO
		pass
	dictionaryFile.close()

def main():
	if sys.argc != 3:
		print "Format: crackzip filename.zip dictionary.txt\n"
		exit(1)

	fileName = sys.argv[1]
	dictionary = sys.argv[2]
	if os.path.exists(fileName) and os.path.isfile(fileName):
		if os.path.exists(dictionaty) and os.path.isfile(dictionary):
			crackZipPassword(fileName)
		else:
			print "Dictionary file '%s' does not exist\n" % (dictionary)
			exit(1)
	else:
		print "File '%s' does not exist\n" % (fileName)
		exit(1)

