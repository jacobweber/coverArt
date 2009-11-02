#!/usr/bin/python

import threading, sys, BaseHTTPServer, select, socket, SocketServer, urllib, cgi, urlparse, pprint, albumDatabase, amazonCoverArt, stpy, hashlib

albumDB = None
albumDBLock = None

class CoverArtWebUIHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	""" Request handler for the Cover Art web interface """

	SERVER_HOST = "localhost"
	SERVER_PORT = 9999

	VALID_TYPES = ('image/jpeg','image/gif')

	def log_message(self, format, *args): pass

	def do_GET(self):
		(scm, netloc, path, params, query, fragment) = urlparse.urlparse(
			self.path, 'http')

		if self.command == "POST":
			cl = int(self.headers['Content-Length'])
			data = self.rfile.read(cl)
			queryParts = cgi.parse_qs(data)
		else:
			queryParts = cgi.parse_qs(query)

		# Display the frame set for our web site.
		if path == '/':
			self.sendTemplate("frameset.tmpl")

		# Display the album list for the left frame of our web site.
		elif path == '/list':
			tags = {"albums":albumDB.getAllRecords(), "urllib":urllib}
			self.sendTemplate("list.tmpl", tags)

		# Display the album details for the right frame of our web site,
		# or save changes to the selected album.
		elif path == '/view' or path == '/save':
			tags = {"response":"", "selection":None, "covers":None, "key":None, "urllib":urllib}
			if "key" not in queryParts:
				self.sendTemplate("album.tmpl", tags)
				return
			tags["key"] = queryParts['key'][0]
			tags["selection"] = albumDB.get(tags["key"])
			if not tags["selection"]:
				tags["response"] = "Album not found"
			elif "searchTerms" not in queryParts:
				aca = amazonCoverArt.AmazonCoverArt()
				tags["covers"] = aca.search(artist=tags["selection"]["artist"], album=tags["selection"]["album"])
				if len(tags["covers"]) == 0:
					tags["response"] = "No covers found"

			if path == '/save':
				albumDBLock.acquire()
				if "clear" in queryParts:
					albumDB.setField(tags["key"], "url", None)
					tags["response"] = 'The cover art was cleared'
				elif "searchTerms" in queryParts:
					aca = amazonCoverArt.AmazonCoverArt()
					tags["covers"] = aca.search(keywords=queryParts["searchTerms"][0])
					if len(tags["covers"]) == 0:
						tags["response"] = "No covers found"
				elif "url" in queryParts:
					albumDB.setField(tags["key"], "url", queryParts["url"][0])
					albumDB.save()
					tags["response"] = 'Your selection was saved'
				else: tags["response"] = 'Unable to save'
				albumDBLock.release()

			self.sendTemplate("album.tmpl", tags)

		# Send an individual album cover image to iTunes.
		elif path == '/serve':
			key = queryParts['key'][0]
			record = albumDB.get(key)
			if record and "url" in record and record["url"] != None:
				self.sendCover(record["url"])
			else: self.sendXML(CoverArtProxyHandler.NO_COVER_FOUND_XML)

		else: self.send_error(404)

	do_POST = do_GET

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
		self.sendXML(CoverArtProxyHandler.NO_COVER_FOUND_XML)

	def sendXML(self, xmlStr):
		self.send_response(200)
		self.send_header('Content-type', 'text/xml; charset=UTF-8')
		self.end_headers()
		self.wfile.write(xmlStr.encode('utf-8'))


class CoverArtProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	""" Request handler for the Cover Art proxy. This acts as a normal web proxy
	for all the system's HTTP requests. However, it intercepts the request that
	iTunes makes for an album cover, and changes the response.
	"""

	SERVER_HOST = "localhost"
	SERVER_PORT = 9988

	rbufsize = 0			# self.rfile will be unbuffered

	COVER_INFO_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Document xmlns="http://www.apple.com/itms/" disableHistory="true" disableNavigation="true">
	<Protocol>
		<plist version="1.0">
			<dict>
				<key>status</key><integer>0</integer>
				<key>cover-art-url</key><string>http://%s:%d/serve?key=%s</string>
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

	def log_message(self, format, *args): pass

	def _connect_to(self, netloc, soc):
		i = netloc.find(':')
		if i >= 0:
			host_port = netloc[:i], int(netloc[i+1:])
		else:
			host_port = netloc, 80
		try: soc.connect(host_port)
		except socket.error, arg:
			try: msg = arg[1]
			except: msg = arg
			self.send_error(404, msg)
			return 0
		return 1

	def do_CONNECT(self):
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			if self._connect_to(self.path, soc):
				self.log_request(200)
				self.wfile.write(self.protocol_version +
					" 200 Connection established\r\n")
				self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
				self.wfile.write("\r\n")
				self._read_write(soc, 300)
		finally:
			soc.close()
			self.connection.close()

	def do_GET(self):
		(scm, netloc, path, params, query, fragment) = urlparse.urlparse(
			self.path, 'http')

		if scm != 'http' or fragment or not netloc:
			self.send_error(400, "bad url %s" % self.path)
			return

		if (path.find('coverArtMatch') != -1):
			# This is called when we choose "Get Album Artwork" in iTunes.
			queryParts = cgi.parse_qs(query)
			if (("an" in queryParts and "pn" in queryParts) or ("a" in queryParts and "p" in queryParts)):
				if ("an" in queryParts):
					# Imported music
					artist = queryParts['an'][0];
					album = queryParts['pn'][0];
				else:
					# Music from iTunes Store
					artist = queryParts['a'][0];
					album = queryParts['p'][0];
				key = hashlib.md5(artist + '/' + album).hexdigest()
				record = albumDB.get(key)
				if record:
					# If we have selected a cover for this album, send a fake XML response
					# to iTunes, to tell it where to get the cover.
					# This response actually points back to our web UI's /serve URL.
					if "url" in record:
						print "Sending iTunes cover for %s / %s" % (artist, album)
						self.sendXML(self.COVER_INFO_XML % (CoverArtWebUIHandler.SERVER_HOST, CoverArtWebUIHandler.SERVER_PORT, urllib.quote_plus(key)))
					else: self.sendXML(self.NO_COVER_FOUND_XML)
					return
				else:
					# If we haven't selected a cover for this album, add it to our database.
					print "iTunes asked for %s / %s" % (artist, album)
					albumDBLock.acquire()
					albumDB.add(key, {"artist":artist, "album":album})
					albumDBLock.release()
					self.sendXML(self.NO_COVER_FOUND_XML)
					return

		# Otherwise, proxy the request to the real destination.
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.proxyRequest(soc);

	def proxyRequest(self, soc):
		(scm, netloc, path, params, query, fragment) = urlparse.urlparse(
			self.path, 'http')
		try:
			if self._connect_to(netloc, soc):
				self.log_request()
				soc.send("%s %s %s\r\n" % (
					self.command,
					urlparse.urlunparse(('', '', path, params, query, '')),
					self.request_version))
				self.headers['Connection'] = 'close'
				del self.headers['Proxy-Connection']
				for key_val in self.headers.items():
					soc.send("%s: %s\r\n" % key_val)
				soc.send("\r\n")
				self._read_write(soc)
		finally:
			soc.close()
			self.connection.close()

	def _read_write(self, soc, max_idling=20):
		iw = [self.connection, soc]
		ow = []
		count = 0
		while 1:
			count += 1
			(ins, _, exs) = select.select(iw, ow, iw, 3)
			if exs: break
			if ins:
				for i in ins:
					if i is soc:
						out = self.connection
					else:
						out = soc
					data = i.recv(8192)
					if data:
						out.send(data)
						count = 0
			if count == max_idling: break

	do_HEAD = do_GET
	do_POST = do_GET
	do_PUT  = do_GET
	do_DELETE=do_GET

	def sendXML(self, xmlStr):
		self.send_response(200)
		self.send_header('Content-type', 'text/xml; charset=UTF-8')
		self.end_headers()
		self.wfile.write(xmlStr.encode('utf-8'))


class StoppableHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
	"""Since this server may be run as a thread, we include a "stop" method,
	to allow it to be stopped from outside the thread.
	"""

	def server_bind(self):
		BaseHTTPServer.HTTPServer.server_bind(self)
		self.socket.settimeout(1)
		self.run = True

	def get_request(self):
		while self.run:
			try:
				sock, addr = self.socket.accept()
				sock.settimeout(None)
				return (sock, addr)
			except socket.timeout:
				if not self.run:
					raise socket.error

	def stop(self):
		self.run = False

	def serve(self):
		while self.run:
			self.handle_request()


def main():
	global albumDB, albumDBLock
	albumDB = albumDatabase.AlbumDatabase()
	albumDBLock = threading.Lock()

	if len(sys.argv) > 1 and sys.argv[1] == "clear":
		print "Clearing local database."
		albumDB.deleteAllRecords()

	try:
		webUIServer = StoppableHTTPServer((CoverArtWebUIHandler.SERVER_HOST, CoverArtWebUIHandler.SERVER_PORT), CoverArtWebUIHandler)
		print "Starting web UI server at http://%s:%d." % (CoverArtWebUIHandler.SERVER_HOST, CoverArtWebUIHandler.SERVER_PORT)
		threading.Thread(target=webUIServer.serve).start()

		proxyServer = StoppableHTTPServer((CoverArtProxyHandler.SERVER_HOST, CoverArtProxyHandler.SERVER_PORT), CoverArtProxyHandler)
		print "Starting proxy server at http://%s:%d." % (CoverArtProxyHandler.SERVER_HOST, CoverArtProxyHandler.SERVER_PORT)
		print "Type control-C to stop."
		proxyServer.serve()
	except KeyboardInterrupt:
		proxyServer.socket.close()
		webUIServer.stop()
		print "\nCoverArt stopped."
	except:
		print "Could not start CoverArt servers: %s" % sys.exc_info()[0]
	albumDB.save()

if __name__ == '__main__':
    main()
