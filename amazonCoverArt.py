#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

import sys, os, urllib, string, xml.dom.minidom, traceback

class AmazonCoverArt(object):
	LICENSE_FILE = "amazonLicense.txt"
	BASE_URLS = {
		"US":"http://webservices.amazon.com/onca/xml?Service=AWSECommerceService",
		"UK":"http://webservices.amazon.co.uk/onca/xml?Service=AWSECommerceService",
		"DE":"http://webservices.amazon.de/onca/xml?Service=AWSECommerceService",
		"JP":"http://webservices.amazon.co.jp/onca/xml?Service=AWSECommerceService",
		"FR":"http://webservices.amazon.fr/onca/xml?Service=AWSECommerceService",
		"CA":"http://webservices.amazon.ca/onca/xml?Service=AWSECommerceService"}
	FULL_URL = string.Template(
		"${baseURL}&AWSAccessKeyId=${accessKey}&Operation=${operation}&SearchIndex=${searchIndex}&"
		+"Title=${title}&Artist=${artist}&Keywords=${keywords}&ResponseGroup=${responseGroup}")

	licenseKey = ""

	def __init__(self):
		if os.access(self.LICENSE_FILE, os.R_OK):
			f = open(self.LICENSE_FILE)
			self.licenseKey = f.readline().strip()
			f.close()

	def search(self, artist='', album='', keywords=''):
		if self.licenseKey == "": return []
		url = self.getURL(artist, album, keywords)
		covers = []
		c = None
		try:
			c = urllib.urlopen(url)
			xmlStr = c.read()
			covers = self.getCovers(xmlStr)
			c.close()
		except:
			if c: c.close()
		return covers

	def getCovers(self, xmlStr):
		covers = []
		usedURLs = []
		try:
			rootNode = xml.dom.minidom.parseString(xmlStr)
			#print rootNode.toprettyxml().encode('ascii', 'ignore')
			itemNodes = rootNode.getElementsByTagName("Item")
			for itemNode in itemNodes:
				for tagName in ("SmallImage","MediumImage","LargeImage"):
					imageNodes = itemNode.getElementsByTagName(tagName)
					for imageNode in imageNodes:
						cover = self.getCoverInfo(imageNode)
						if cover["url"] not in usedURLs:
							covers.append(cover)
							usedURLs.append(cover["url"])
		except:
			traceback.print_exc(file=sys.stdout)
			raise
		return covers

	def getCoverInfo(self, imageNode):
		cover = {}
		cover["url"] = imageNode.getElementsByTagName("URL")[0].childNodes[0].data
		cover["w"] = imageNode.getElementsByTagName("Height")[0].childNodes[0].data
		cover["h"] = imageNode.getElementsByTagName("Width")[0].childNodes[0].data
		return cover

	def getURL(self, artist, album, keywords):
		d = {}
		d['baseURL'] = self.BASE_URLS['US']
		d['accessKey'] = self.licenseKey
		d['operation'] = 'ItemSearch'
		d['searchIndex'] = 'Music'
		d['responseGroup'] = 'Images'
		d['keywords'] = urllib.quote_plus(keywords)
		d['artist'] = urllib.quote_plus(artist)
		d['title'] = urllib.quote_plus(album)
		return self.FULL_URL.substitute(d)

def main():
	aca = AmazonCoverArt()
	# sample search
	covers = aca.search('Elvis Costello', 'My Aim Is True')
	for cover in covers:
		print cover["url"]

if __name__ == '__main__':
    main()
