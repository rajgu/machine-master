from src.db.Crud import Crud


class DBStpOwners(Crud):


	_table_name = 'stp_owners'


	_table_struct = {
		'stp_id'       : {'type' : 'integer', 'validate' : True},
		'user_id'      : {'type' : 'integer', 'validate' : True}
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
