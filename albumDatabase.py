import os, pickle

class AlbumDatabase(object):
	""" Maintains a flat-file database of album covers. """

	FILE_NAME = "albumDatabase.pkl"

	data = None

	def __init__(self):
		self.load()

	def deleteAllRecords(self):
		self.data = {}

	def load(self):
		if os.access(self.FILE_NAME, os.R_OK):
			f = open(self.FILE_NAME, 'rb')
			self.data = pickle.load(f)
			f.close()
		else: self.data = {}

	def save(self):
		f = open(self.FILE_NAME, 'wb')
		pickle.dump(self.data, f)
		f.close()

	def get(self, key):
		if key not in self.data: return None
		return self.data[key]

	def add(self, key, data):
		if key not in self.data:
			self.data[key] = data

	def setField(self, key, field, value):
		if key not in self.data: return
		self.data[key][field] = value

	def getAllRecords(self):
		for key in self.data:
			yield (key, self.data[key])
