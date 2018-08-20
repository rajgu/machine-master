import ConfigParser
import logging
import os

class Config:

	def __init__(self, fname=False):

		if fname == False:
			self.fname = "config.ini"

		self.parser = ConfigParser.SafeConfigParser()

		if os.path.isfile(self.fname):
			self.parser.read(self.fname)
		else:
			raise ("Please fill config file {0}".format(self.fname))

		# Initialize logging
		logging.basicConfig(format=self.get('logging.format'), filename=self.get('logging.filename'), level=self.get('logging.level'))


	def get(self, what):
		section, option = what.split('.')
		value = self.parser.get(section, option)
		if value == 'True':
			return True
		if value == 'False':
			return False

		return value
