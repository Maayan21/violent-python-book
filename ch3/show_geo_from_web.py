import os
import sys
import urllib2
from bs4 import BeautifulSoup
from os.path import basename
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
from urlparse import urlsplit

#
# Some ideas and code from https://gist.github.com/erans/983821#file-get_lat_lon_exif_pil-py-L33
#

def convert_to_degrees(value):
	"""
	Converts GPS data in EXIF to degrees
	"""
	d0 = value[0][0]
	d1 = value[0][1]
	if d1 == 0:
		return 0
	d = float(d0) / float(d1)

	m0 = value[1][0]
	m1 = value[1][1]
	if m1 == 0:
		return 0
	m = float(m0) / float(m1)

	s0 = value[2][0]
	s1 = value[2][1]
	if s1 == 0:
		return 0
	s = float(s0) / float(s1)

	return d + (m / 60.0) + (s / 3600.0)



def show_geodata_for_image(imageSrc, imageFilePath):
	"""
	Searches for GPS data in the image and shows it if found and valid.
	"""
	exitData = {}
	try:
		imageFile = Image.open(imageFilePath)
		info = imageFile._getexif()
	except:
		return

	if info:
		for (tag, value) in info.items():
			decoded = TAGS.get(tag, tag)
			if decoded == 'GPSInfo':
				gpsData = {}
				for t in value:
					decodedGps = GPSTAGS.get(t, t)
					gpsData[decodedGps] = value[t]

				if 'GPSLatitude' in gpsData and 'GPSLatitudeRef' in gpsData and 'GPSLongitude' in gpsData and 'GPSLongitudeRef' in gpsData:
					latitude = convert_to_degrees(gpsData['GPSLatitude'])
					if gpsData['GPSLatitudeRef'] != 'N':
						latitude = 0 - latitude
					longitude = convert_to_degrees(gpsData['GPSLongitude'])
					if gpsData['GPSLongitude'] != 'E':
						longitude = 0 - longitude
					if latitude !=0 and longitude != 0:
						print 'GPS data for %s: latitude=%f%s, longitude=%f%s' % (imageSrc, latitude, gpsData['GPSLatitudeRef'], longitude, gpsData['GPSLongitudeRef'])

				break


def process_image(imageTag):
	"""
	Processes a single image in the tag
	"""
	try:
		src = imageTag['src']
	except:
		return

	imageFileName = basename(urlsplit(src)[2])
	if imageFileName == '':
		return

	try:
		imageContent = urllib2.urlopen(src).read()
	except:
		return

	imageFile = open(imageFileName, 'wb')
	imageFile.write(imageContent)
	imageFile.close()

	show_geodata_for_image(src, imageFileName)

	os.unlink(imageFileName)


def find_and_process_images(url):
	"""
	Finds and processes images inside the content from the given url
	"""
	images = []
	imageTags = []
	try:
		urlContent = urllib2.urlopen(url).read()
		parser = BeautifulSoup(urlContent, 'html.parser')
		imageTags = parser.findAll('img')
	except Exception, e:
		print 'Unable to read the url: ' + str(e)

	for tag in imageTags:
		process_image(tag)


def main():
	if len(sys.argv) == 2:
		find_and_process_images(sys.argv[1])
	else:
		print "Usage: " + basename(sys.argv[0]) + " url"


main()

