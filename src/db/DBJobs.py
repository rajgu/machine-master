from src.db.Crud import Crud


class DBJobs(Crud):


	_table_name = 'jobs'


	_table_struct = {
		'id'                : {'type' : 'integer', 'validate' : True},
		'event'             : {'type' : 'text',    'validate' : True},
		'time_test'         : {'type' : 'text',    'validate' : False},
		'time_prep'         : {'type' : 'text',    'validate' : False},
		'time_utilization'  : {'type' : 'text',    'validate' : False},
		'du'                : {'type' : 'text',    'validate' : True},
		'duplex'            : {'type' : 'text',    'validate' : True},
		'up'                : {'type' : 'text',    'validate' : True},
		'type'              : {'type' : 'text',    'validate' : True},
		'inst_type'         : {'type' : 'text',    'validate' : True},
		'date_created'      : {'type' : 'text',    'validate' : True},
		'date_finished'     : {'type' : 'text',    'validate' : True},
		'date_rcm_install'  : {'type' : 'text',    'validate' : True},
		'date_started'      : {'type' : 'text',    'validate' : True},
# Jobs Properties:
		'prop_up'           : {'type' : 'text',    'validate' : False},
		'ip_version'        : {'type' : 'text',    'validate' : False},
		'criteria'          : {'type' : 'text',    'validate' : False},
		'priority'          : {'type' : 'integer', 'validate' : False},
		'stp'               : {'type' : 'text',    'validate' : False},
		'owner'             : {'type' : 'integer', 'validate' : False},
		'use_stp'           : {'type' : 'text',    'validate' : False},
		'force_install'     : {'type' : 'text',    'validate' : False}

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
