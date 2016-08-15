import pyPdf
import sys

def printMetaData(pdfFileName):
	try:
		pdfFile = pyPdf.PdfFileReader(file(pdfFileName, 'rb'))
	except:
		print 'Cannot open the file'
		return

	docInfo = pdfFile.getDocumentInfo()
	for item in docInfo:
		print '  %s: %s' % (item.lstrip('/'), docInfo[item])

def main():
	if len(sys.argv) <> 2:
		print 'Missing file name on the command line'
	else:
		printMetaData(sys.argv[1])

main()

