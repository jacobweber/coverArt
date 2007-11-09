#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

import BaseHTTPServer, urllib, cgi, urlparse, pprint, albumDatabase, amazonCoverArt, stpy, md5

albumDB = None

class CoverArtServer(BaseHTTPServer.BaseHTTPRequestHandler):
	SERVER_PORT = 80

	VALID_TYPES = ('image/jpeg','image/gif')

	STORE_BAG_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Document xmlns="http://www.apple.com/itms/">
	<Protocol>
		<plist version="1.0">
			<dict>
				<key>jingleDocType</key><string>initiateSessionSuccess</string>
				<key>jingleAction</key><string>mzInitiateSession</string>
				<key>urlBag</key>
				<dict>
					<key>storeFront</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/storeFront</string>
					<key>newUserStoreFront</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/storeFront</string>
					<key>newIPodUserStoreFront</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/newIPodUser?newIPodUser=true</string>
					<key>newPhoneUser</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/phoneLandingPage</string>                  
					<key>search</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/DirectAction/search</string>
					<key>advancedSearch</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/DirectAction/advancedSearch</string>
					<key>parentalAdvisory</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/parentalAdvisory</string>
					<key>songMetaData</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/songMetaData</string>
					<key>browse</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/browse</string>
					<key>browseStore</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/browseStore</string>
					<key>browseGenre</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/browseGenre</string>
					<key>browseArtist</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/browseArtist</string>
					<key>browseAlbum</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/browseAlbum</string>
					<key>viewAlbum</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewAlbum</string>
					<key>viewArtist</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewArtist</string>
					<key>viewComposer</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewComposer</string>
					<key>viewGenre</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewGenre</string>
					<key>viewPodcast</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewPodcast</string>
					<key>viewPublishedPlaylist</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewPublishedPlaylist</string>
					<key>viewVideo</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewVideo</string>
					<key>podcasts</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewPodcastDirectory</string>
					<key>externalURLSearchKey</key><string>ax.phobos.apple.com.edgesuite.net</string>
					<key>externalURLReplaceKey</key><string>phobos.apple.com</string>
					<key>libraryLink</key><string>http://phobos.apple.com/WebObjects/MZSearch.woa/wa/DirectAction/libraryLink</string>
					<key>selectedItemsPage</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/selectedItemsPage</string>
					<key>ministore</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/ministoreV2</string>
					<key>ministore-fields</key><string>a,kind,p</string>
					<key>ministore-match</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/ministoreMatchV2</string>
					<key>ministore-match-fields</key><string>an,gn,kind,pn</string>
					<key>mini-store-welcome</key><string>http://phobos.apple.com/WebObjects/MZStore.woa/wa/ministoreClientOptIn</string>
					<key>mini-store</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/ministoreV2</string>
					<key>mini-store-fields</key><string>a,kind,p</string>
					<key>mini-store-match</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/ministoreMatchV2</string>
					<key>mini-store-match-fields</key><string>an,gn,kind,pn</string>
					<key>cover-art</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/coverArtMatch</string>
					<key>cover-art-fields</key><string>a,p</string>
					<key>cover-art-match</key><string>http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/coverArtMatch</string>
					<key>cover-art-match-fields</key><string>cddb,an,pn</string>
					<key>maxComputers</key><string>5</string>
					<key>maxPublishedPlaylistItems</key><integer>250</integer>
					<key>trustedDomains</key>
					<array>
						<string>.apple.com</string>
						<string>.apple.com.edgesuite.net</string>
						<string>support.mac.com</string>
						<string>.itunes.com</string>
						<string>itunes.com</string>
						<string>click.linksynergy.com</string>
					</array>
				</dict>
			</dict>
		</plist>
	</Protocol>
</Document>'''

	COVER_INFO_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Document xmlns="http://www.apple.com/itms/" disableHistory="true" disableNavigation="true">
	<Protocol>
		<plist version="1.0">
			<dict>
				<key>status</key><integer>0</integer>
				<key>cover-art-url</key><string>http://localhost/serve?key=%s</string>
				<key>request-delay-seconds</key><string>.1</string>
				<key>artistName</key><string></string>
				<key>playlistName</key><string></string>
				<key>artistId</key><string></string>
				<key>playlistId</key><string></string>
				<key>matchType</key><string>2</string>
			</dict>
		</plist>
	</Protocol>
</Document>'''

	NO_COVER_FOUND_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Document xmlns="http://www.apple.com/itms/" disableHistory="true" disableNavigation="true">
	<Protocol>
		<plist version="1.0">
			<dict>
				<key>status</key><integer>3004</integer>
				<key>cover-art-url</key><string></string>
				<key>request-delay-seconds</key><string>.1</string>
			</dict>
		</plist>
	</Protocol>
</Document>'''

	def do_GET(self):
		print self.headers['Host']
		urlParts = urlparse.urlparse(self.path)
		location = urlParts[2]
		query = cgi.parse_qs(urlParts[4])
		self.handleRequest(location, query)

	def do_POST(self):
		print self.headers['Host']
		urlParts = urlparse.urlparse(self.path)
		location = urlParts[2]
		cl = int(self.headers['Content-Length'])
		data = self.rfile.read(cl)
		query = cgi.parse_qs(data)
		self.handleRequest(location, query)

	def handleRequest(self, location, query):
		if location == '/':
			self.sendTemplate("frameset.tmpl")

		elif location == '/list':
			tags = {"albums": albumDB.getAllRecords(), "urllib":urllib}
			self.sendTemplate("list.tmpl", tags)

		elif location == '/view' or location == '/save':
			tags = {"response":"", "selection":None, "covers":None, "key":None, "urllib":urllib}
			if "key" not in query:
				self.sendTemplate("album.tmpl", tags)
				return
			tags["key"] = query['key'][0]
			tags["selection"] = albumDB.get(tags["key"])
			if not tags["selection"]:
				tags["response"] = "Album not found"
			elif "searchTerms" not in query:
				aca = amazonCoverArt.AmazonCoverArt()
				tags["covers"] = aca.search(artist=tags["selection"]["artist"], album=tags["selection"]["album"])
				if len(tags["covers"]) == 0:
					tags["response"] = "No covers found"

			if location == '/save':
				if "clear" in query:
					albumDB.setField(tags["key"], "url", "")
					tags["response"] = 'The cover art was cleared'
				elif "searchTerms" in query:
					aca = amazonCoverArt.AmazonCoverArt()
					tags["covers"] = aca.search(keywords=query["searchTerms"][0])
					if len(tags["covers"]) == 0:
						tags["response"] = "No covers found"
				elif "url" in query:
					albumDB.setField(tags["key"], "url", query["url"][0])
					albumDB.save()
					tags["response"] = 'Your selection was saved'
				else: tags["response"] = 'Unable to save'

			self.sendTemplate("album.tmpl", tags)

		elif location == '/serve':
			key = query['key'][0]
			record = albumDB.get(key)
			if record and "url" in record:
				self.sendCover(record["url"])
			else: self.sendXML(self.NO_COVER_FOUND_XML)

		elif location == '/storeBag.xml.gz':
			self.sendXML(self.STORE_BAG_XML)
			pass

		elif location == '/WebObjects/MZSearch.woa/wa/coverArtMatch':
			key = md5.new(query['an'][0] + '/' + query['pn'][0]).hexdigest()
			record = albumDB.get(key)
			if record:
				if "url" in record:
					self.sendXML(self.COVER_INFO_XML % urllib.quote_plus(key))
				else: self.sendXML(self.NO_COVER_FOUND_XML)
			else:
				albumDB.add(key, {"artist":query['an'][0], "album":query['pn'][0]})
				self.sendXML(self.NO_COVER_FOUND_XML)

		else: self.send_error(404)

	def sendXML(self, xmlStr):
		self.send_response(200)
		self.send_header('Content-type', 'text/xml; charset=UTF-8')
		self.end_headers()
		self.wfile.write(xmlStr.encode('utf-8'))

	def sendTemplate(self, tmplFile, tags = {}):
		f = open(tmplFile, 'r')
		text = f.read()
		f.close()
		tmpl = stpy.Template(text)
		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=UTF-8')
		self.end_headers()
		print >> self.wfile, tmpl.render(tags)

	def sendCover(self, url):
		try:
			f = None
			f = urllib.urlopen(url)
			type = f.info().gettype()
			if type in self.VALID_TYPES:
				imgData = f.read()
				f.close()
				self.send_response(200)
				self.send_header('Content-type', type)
				self.end_headers()
				self.wfile.write(imgData)
				return
		except:
			print "Can't read image"
			if f: f.close()
		self.sendXML(self.NO_COVER_FOUND_XML)

def main():
	global albumDB
	albumDB = albumDatabase.AlbumDatabase()
	try:
		server = BaseHTTPServer.HTTPServer(('', CoverArtServer.SERVER_PORT), CoverArtServer)
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
	except:
		print "Could not start server"
	albumDB.save()

if __name__ == '__main__':
    main()
