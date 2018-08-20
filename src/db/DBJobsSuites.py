from src.db.Crud import Crud


class DBJobsSuites(Crud):


	_table_name = 'jobs_suites'


	_table_struct = {
		'job_id'            : {'type' : 'integer', 'validate' : True},
		'suite'             : {'type' : 'text',    'validate' : True},
		'ok'                : {'type' : 'integer', 'validate' : False},
		'nok'               : {'type' : 'integer', 'validate' : False},
		'skip'              : {'type' : 'integer', 'validate' : False}
	}


	_horizontal_key = False


	def __init__(self, db):
		return Crud.__init__(self, db)


	def create(self, data):
		return Crud.create(self, data, self._table_name, self._table_struct, self._horizontal_key)


	def read(self, data, oldata=False):
		return Crud.read(self, data, self._table_name, self._table_struct, self._horizontal_key, oldata)


	def update(self, data, where):
		return Crud.update(self, data, where, self._table_name, self._table_struct, self._horizontal_key)


	def delete(self, data):
		return Crud.delete(self, data, self._table_name, self._table_struct, self._horizontal_key)
