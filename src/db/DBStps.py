from src.db.Crud import Crud


class DBStps(Crud):


	_table_name = 'stps'


	_table_struct = {
		'id'                    : {'type' : 'integer', 'validate' : True},
		'name'                  : {'type' : 'text',    'validate' : True},
		'board_type'            : {'type' : 'text',    'validate' : True},
		'duplex_type'           : {'type' : 'text',    'validate' : True},
		'site'                  : {'type' : 'text',    'validate' : True},
		'worker'                : {'type' : 'text',    'validate' : True},
		'customer_organization' : {'type' : 'text',    'validate' : True},
		'last_update'           : {'type' : 'text',    'validate' : True},
		'eris_url'              : {'type' : 'text',    'validate' : True},
		'worker_log'            : {'type' : 'text',    'validate' : True},
		'type'                  : {'type' : 'text',    'validate' : True},
		'site_lan_ip'           : {'type' : 'text',    'validate' : True},
		'status'                : {'type' : 'text',    'validate' : True},
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
