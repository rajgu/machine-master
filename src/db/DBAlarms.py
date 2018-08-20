from src.db.Crud import Crud


class DBAlarms(Crud):


    _table_name = 'alarms'


    _table_struct = {
        'id':                      {'type' : 'integer', 'validate' : True},
        'stp_id':                  {'type' : 'integer', 'validate' : True},
        'date_notice_start':       {'type' : 'text',    'validate' : True},
        'date_notice_end':         {'type' : 'text',    'validate' : True},
        'alarm_id':                {'type' : 'integer', 'validate' : True},
        'event_time':              {'type' : 'text',    'validate' : True},
        'perceived_severity' :     {'type' : 'text',    'validate' : True},
        'managed_object_class':    {'type' : 'text',    'validate' : True},
        'managed_object_instance': {'type' : 'text',    'validate' : True},
        'specific_problem':        {'type' : 'text',    'validate' : True},
        'probable_cause':          {'type' : 'text',    'validate' : True},
        'additional_text':         {'type' : 'text',    'validate' : True},
        'acknowledged_by':         {'type' : 'text',    'validate' : True},
        'acknowledgement_time':    {'type' : 'text',    'validate' : True},
        'acknowledgement_state':   {'type' : 'text',    'validate' : True},
        'system_dn':               {'type' : 'text',    'validate' : True},
        'notification_id':         {'type' : 'integer', 'validate' : True},
        'additional_info':         {'type' : 'text',    'validate' : True}
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
