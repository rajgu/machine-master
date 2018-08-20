from src.db.Crud import Crud


class DBUsers(Crud):


	_table_name = 'users'


	_table_struct = {
		'id'           : {'type' : 'integer', 'validate' : True},
		'signum'       : {'type' : 'text',    'validate' : True},
		'email'        : {'type' : 'text',    'validate' : True},
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
