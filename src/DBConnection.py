import sqlite3
import time
import logging

class DBConnection:

	def __init__(self, config):

		self.dbname       = config.get('database.name');
		self.debug        = config.get('database.debug');
		self.autocommit   = config.get('database.autocommit');
		self.row_factory  = config.get('database.row_factory');
		self.foreign_keys = config.get('database.foreign_keys');
		self.retry_limit  = int(config.get('database.retry_limit'));
		self.retry_time   = float(config.get('database.retry_time'));



	def connect(self):

		if self.debug:
			logging.debug("Connecting to '{0}', debug: '{1}', autocommit: '{2}'".format(self.dbname, self.debug, self.autocommit))

		self.connection = sqlite3.connect(self.dbname)
		if self.row_factory:
			self.connection.row_factory = self._dict_factory

		self.connection.text_factory = str

		self.cursor = self.connection.cursor()

		if self.debug:
			result = self.execute('SELECT SQLITE_VERSION()')
			if self.row_factory:
				logging.debug("SQLite version (Database): {0}".format(result[0]['SQLITE_VERSION()']))
			else:
				logging.debug("SQLite version (Database): {0}".format(result[0][0]))

		self.setForeignKeys(self.foreign_keys)

		return self


	def execute(self, query):

		logging.debug("Executing query: {0}".format(query))

		if query[0:6] == 'SELECT':
			if self.debug:
				logging.debug('Enter SELECT strategy')

			self._saveExec(query)

			data = self.cursor.fetchall()
			if self.debug:
				logging.debug('Returning {0} records, data: {1}'.format(len(data), data))

			return data

		elif query[0:6] == 'INSERT':
			if self.debug:
				logging.debug('Enter INSERT strategy')

			self._saveExec(query)

			count = self.cursor.rowcount

			if self.debug:
				logging.debug("Inserted {0} records".format(count))
			if self.autocommit and count != 0:
				logging.debug('Commiting transaction')
				self.connection.commit()

			return count

		elif query[0:6] == 'UPDATE':
			if self.debug:
				logging.debug('Enter UPDATE strategy')

			self._saveExec(query)

			count = self.cursor.rowcount

			if self.debug:
				logging.debug("Updated {0} records".format(count))
			if self.autocommit and count != 0:
				logging.debug('Commiting transaction')
				self.connection.commit()

			return count

		elif query[0:6] == 'DELETE':
			if self.debug:
				logging.debug('Enter DELETE strategy')

			self._saveExec(query)

			count = self.cursor.rowcount

			if self.debug:
				logging.debug("Deleted {0} records".format(count))
			if self.autocommit and count != 0:
				logging.debug('Commiting transaction')
				self.connection.commit()

			return count

		elif query[0:6] == 'PRAGMA':
			if self.debug:
				logging.debug('Enter PRAGMA strategy')

			self._saveExec(query)

		else:
			raise Exception("Cant recognize query type {0}".format(query))


	def _saveExec(self, query):

		for i in range(0, self.retry_limit):
			try:
				return self.cursor.execute(query)
			except sqlite3.OperationalError as e:
				logging.info("SQL Query exception: {0}/{1}, Exception:'{2}', executing query: {3}".format(i, self.retry_limit, e, query))
				time.sleep (self.retry_time)
			except sqlite3.Error as e:
				logging.fatal("SQL Query Unrecognized exception: '{0}', executing query: {1}".format(e, query))
				break
		raise Exception("Exception:'{0}', executing query: '{1}'".format(e, query))


	def getAutocommit(self):
		return self.autocommit


	def setAutocommit(self, autocommit):
		if not autocommit in [True, False]:
			raise Exception("Bad autocommit value: {0}, expected True/False".format(autocommit))

		self.autocommit = autocommit


	def commit(self):
		if self.autocommit and not self.debug:
			logging.warning("Manual commiting with autocommit enabled")
		else:
			logging.debug("Comitting transaction")
		return self.connection.commit()


	def setForeignKeys(self, status):
		if status:
			pragma = 'ON'
		else:
			pragma = 'OFF'

		return self.execute("PRAGMA foreign_keys = {0}".format(pragma))


	def _dict_factory(self, cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d



	def __exit__(self, exc_type, exc_value, traceback):
		self.commit()
