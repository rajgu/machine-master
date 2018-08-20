class Crud(object):


    _bool_operators = [
        'is',
        'is not',
    ]


    def __init__(self, db):
        self.db = db



    def create(self, data, tname, tstruct, horizontal_key):

        self._parse_input_data(data, tname, tstruct, horizontal_key)

        querries = []

        if horizontal_key:

            horizontal_value = data[horizontal_key]
            del data[horizontal_key]

            for key, value in data.iteritems():
                if isinstance(value, list):
                    for elem in value:
                        querries.append("INSERT INTO `{0}` (`{1}`, `key`, `value`) VALUES ('{2}', '{3}', '{4}')".format(tname, horizontal_key, horizontal_value, key, elem))
                else:
                    querries.append("INSERT INTO `{0}` (`{1}`, `key`, `value`) VALUES ('{2}', '{3}', '{4}')".format(tname, horizontal_key, horizontal_value, key, value))

        else:

            fields = []
            values = []

            if isinstance(data, list):

                if isinstance(data[0], dict):

                    for instance in data:
                        if not isinstance(instance, dict):
                            raise Exception ("Data: {0} is not dictionary".format(instance))

                    tableKeys = []
                    for singleData in data:
                        for key, value in singleData.iteritems():
                            tableKeys.append(key)

                    tableKeys = list(set(tableKeys))

                    for singleData in data:
                        singleInsertData = []
                        for key in tableKeys:
                            if key in singleData:
                                singleInsertData.append(str(singleData[key]))
                            else:
                                singleInsertData.append('')

                        querries.append("INSERT INTO `{0}` (`{1}`) VALUES ('{2}')".format(tname, '`, `'.join(tableKeys),  "', '".join(singleInsertData)))

                else:

                    for key, value in data[0].iteritems():
                        fields.append(key)

                    ins_array = []
                    for item in data:
                        tmp = []
                        for key in fields:
                            tmp.append(item[key])
                        querries.append("INSERT INTO `{0}` (`{1}`) VALUES ({2})".format(tname, '`, `'.join(fields),  "', '".join(tmp)))

            elif isinstance(data, dict):

                for key, value in data.iteritems():
                    fields.append(key)
                    values.append(str(value))

                querries.append("INSERT INTO `{0}` (`{1}`) VALUES ('{2}')".format(tname, '`, `'.join(fields),  "', '".join(values)))

        for query in querries:
            self.db.execute(query)

        return True


    def read(self, data, tname, tstruct, horizontal_key, other_data):

        self._parse_input_data(data, tname, tstruct, horizontal_key)

        if len(data):
            where = " WHERE {0}".format(self._build_simple_where(data))
        else:
            where = ''

        if other_data != False and len(other_data):
            olimit  = self._build_simple_order_limit(other_data, tname, tstruct)
            groupBy = self._build_simple_group_by(other_data, tname, tstruct)
            select  = self._build_simple_select(other_data, tname, tstruct)
            join    = self._build_simple_join(other_data, tname)

        else:
            olimit  = ''
            groupBy = ''
            select  = 'SELECT *'
            join    = ''

        query = "{0} FROM `{1}`{2}{3}{4}{5}".format(select, tname, join, where, groupBy, olimit)

        return self._transform_return_data(self.db.execute(query), tstruct, horizontal_key, other_data)


    def update(self, data, where, tname, tstruct, horizontal_key):

        if not len(data):
            raise Exception("No data to update")

        self._parse_input_data(data, tname, tstruct, horizontal_key)
        self._parse_input_data(where, tname, tstruct, horizontal_key)

        update = []
        for key, value in data.iteritems():
            update.append("`{0}` = '{1}'".format(key, value))

        if len(where):
            where = " WHERE {0}".format(self._build_simple_where(where))
        else:
            where = ''

        query = "UPDATE `{0}` SET {1} {2}".format(tname, ", ".join(update), where)

        return self.db.execute(query)



    def delete(self, data, tname, tstruct, horizontal_key):

        if not len(data):
            raise Exception("Cant delete data without where")

        self._parse_input_data(data, tname, tstruct, horizontal_key)
        where = self._build_simple_where(data)

        query = "DELETE FROM `{0}` WHERE {1}".format(tname, where)

        return self.db.execute(query)



    def execute(self, query):
        return self.db.execute



    def _build_simple_order_limit(self, data, tname, tstruct):

        if not isinstance(data, dict):
            raise Exception("Data: '{0}' is not dictionary".format(str(data)))

        order = ''

        if 'order' in data:
            if not isinstance(data['order'], str):
                raise Exception("Param order is not string: '{0}'".format(str(data['order'])))

            if not data['order'] in tstruct:
                raise Exception("Field: '{0}' (order) not exists in definition of table: '{1}'".format(data['order'], tname))

            if 'sort' in data:
                if not isinstance(data['sort'], str):
                    raise Exception("Param sort is not string: '{0}'".format(str(data['sort'])))

                if not data['sort'].lower() in ['asc', 'desc']:
                    raise Exception("Param sort is different than ASC/DESC: '{0}'".format(str(data['sort'])))

                order = " ORDER BY `{0}` {1}".format(data['order'], data['sort'])
            else:
                order = " ORDER BY `{0}`".format(data['order'])

        limit = ''

        if 'limit' in data:
            if isinstance(data['limit'], int):
                limit = " LIMIT {0}".format(data['limit'])
            elif isinstance(data['limit'], list):
                if len(data['limit']) != 2 or not isinstance(data['limit'][0], int)  or not isinstance(data['limit'][1], int):
                    raise Exception("Bad parameters passed to limit: {0}".format(str(data['limit'])))
                limit = " LIMIT {0},{1}".format(data['limit'][0], data['limit'][1])
            else:
                raise Exception("Limit is not int/list: '{0}'".format(str(data['limit'])))

        return "{0}{1}".format(order, limit)


    def _build_simple_where(self, param):

        tmp = []

        if isinstance(param, list):
            for pos in param:
                if isinstance(pos, list):
                    if len(pos) == 2:
                        tmp.append("{0} = '{1}'".format(pos[0], pos[1]))
                    elif len(pos) == 3:
                        if pos[1].lower() in self._bool_operators:
                            tmp.append("{0} {1} {2}".format(pos[0], pos[1], pos[2]))
                        else:
                            tmp.append("{0} {1} '{2}'".format(pos[0], pos[1], pos[2]))
                    else:
                        raise Exception("Wrong argument list count: {0}".format(pos))
                elif isinstance(pos, dict):
                    for key, value in pos.iteritems():
                        tmp.append("{0} = '{1}'".format(key, value))

        elif isinstance(param, dict):
            for key, value in param.iteritems():
                if isinstance(value, list):
                    trk = []
                    for elem in value:
                        if isinstance(elem, str):
                            trk.append("'{0}'".format(elem))
                        else:
                            trk.append(str(elem))
                    tmp.append("{0} IN ({1})".format(key, ", ".join(trk)))
                else:
                    tmp.append("{0} = '{1}'".format(key, value))

        else:
            raise Exception("Wrong argument list count: {0}".format(param))

        return " AND ".join(tmp)



    def _parse_input_data(self, data, tname, tstruct, horizontal_key):

        if horizontal_key:

            if not horizontal_key in data:
                raise Exception("Horizontal key '{0}' not passed in query data '{1}'".format(horizontal_key, data))

        else:
            if isinstance(data, list):

                for pos in data:
                    if isinstance(pos, list):

                        if not pos[0] in tstruct:
                            raise Exception("Key {0} does not exists in definition of table {1}".format(pos[0], tname))

                        if len(pos) == 2 or len(pos) == 3:
                            if tstruct[pos[0]]['validate'] and tstruct[pos[0]]['type'] == 'string' and not isinstance(pos[-1], str):
                                raise Exception("Value: '{0}' is not an string".format(pos[-1]))
                            elif tstruct[pos[0]]['validate'] and tstruct[pos[0]]['type'] == 'integer' and not (isinstance(pos[-1], int) or (isinstance(pos[-1], str) and pos[-1].isdigit())):
                                raise Exception("Value: '{0}' is not an integer".format(pos[-1]))
                        else:
                            raise Exception("Wrong argument list count: {0}".format(pos))

                    elif isinstance(pos, dict):
                        for key, value in pos.iteritems():

                            if not key in tstruct:
                                raise Exception("Key {0} does not exists in definition of table {1}".format(key, tname))

                            if tstruct[key]['validate'] and tstruct[key]['type'] == 'string' and not isinstance(value, str):
                                raise Exception("Value: '{0}' is not an string".format(value))
                            elif tstruct[key]['validate'] and tstruct[key]['type'] == 'integer' and not (isinstance(value, int) or (isinstance(value, str) and value.isdigit())):
                                raise Exception("Value: '{0}' is not an integer".format(value))

                    else:
                        raise Exception("Param is not a list")

            elif isinstance(data, dict):
                for key, value in data.iteritems():

                    if '.' in key:
                        key = key.split('.')[1]

                    if not key in tstruct:
                        raise Exception("Key {0} does not exists in definition of table {1}".format(key, tname))

                    if isinstance(value, list):
                        for val in value:
                            if tstruct[key]['validate'] and tstruct[key]['type'] == 'string' and not isinstance(val, str):
                                raise Exception("Value: '{0}' is not an string".format(val))
                            elif tstruct[key]['validate'] and tstruct[key]['type'] == 'integer' and (isinstance(val, int) and (isinstance(val, str) and val.isdigit())):
                                raise Exception("Value: '{0}' is not an integer".format(val))
                    else:
                        if tstruct[key]['validate'] and tstruct[key]['type'] == 'string' and not isinstance(value, str):
                            raise Exception("Value: '{0}' is not an string".format(value))
                        elif tstruct[key]['validate'] and tstruct[key]['type'] == 'integer' and (isinstance(value, int) and (isinstance(value, str) and value.isdigit())):
                            raise Exception("Value: '{0}' is not an integer, key: '{1}'".format(value, key))
            else:
                raise Exception("Data is not dictionary/list type")


    def _build_simple_group_by(self, data, tname, tstruct):

        if 'groupBy' in data:
            if isinstance(data['groupBy'], str):
                if not data['groupBy'] in tstruct:
                    raise Exception("Field: '{0}' does not exists in definition of table {1}".format(data['groupBy'], tname))
                groupBy = "`{0}`".format(data['groupBy'])
            elif isinstance(data['groupBy'], list):
                for field in data['groupBy']:
                    if not field in tstruct:
                        raise Exception("Field: '{0}' does not exists in definition of table {1}".format(field, tname))
                groupBy = "{0}".format(", ".join(data['groupBy']))
            else:
                raise Exception("groupBy: unsupported type: '{0}'".format(type(data['groupBy'])))
            return ' GROUP BY {0}'.format(groupBy)
        else:
            return ''


    # fields - select / count on selected fields
    # count - Bool - do the count operation?
    # distinct - Bool - add the distinct parameter?

    def _build_simple_select(self, data, tname, tstruct):

        if 'fields' in data:
            if isinstance(data['fields'], str):
                if not data['fields'] in tstruct:
                    raise Exception("Field: '{0}' does not exists in definition of table {1}".format(data['fields'], tname))
                fields = "`{0}`".format(data['fields'])
            elif isinstance(data['fields'], list):
                for field in data['fields']:
                    if not field in tstruct and field[0:5].lower() != 'count':
                        raise Exception("Field: '{0}' does not exists in definition of table {1}".format(field, tname))
                fields = "{0}".format(", ".join(data['fields']))
            else:
                raise Exception("Field: 'fields' unsupported type: '{0}'".format(type(data['fields'])))
        else:
            fields = '*'

        if 'distinct' in data:
            if not isinstance(data['distinct'], bool):
                raise Exception("Field: 'distinct' unsupported type: '{0}'".format(type(data['distinct'])))

        if 'count' in data:
            if not isinstance(data['count'], bool):
                raise Exception("Field: 'count' unsupported type: '{0}'".format(type(data['count'])))

        if 'distinct' in data and data['distinct']:
            if 'count' in data and data['count'] == True:
                return "SELECT COUNT(DISTINCT({0})) AS count".format(fields)
            else:
                return "SELECT DISTINCT({0})".format(fields)
        else:
            if 'count' in data and data['count'] == True:
                return "SELECT COUNT({0}) AS count".format(fields)
            else:
                return "SELECT {0}".format(fields)


    # Struktura:
    # Wymagane przekazanie listy
    # 0 - Dolaczona tabela
    # 1 - Pole po ktorym laczymy zrodlowa tabele
    # 2 - Pole po ktorym laczymy docelowa tabele
    def _build_simple_join(self, other_data, tname):
        if other_data and 'join' in other_data:
            return ' JOIN `{0}` ON `{1}`.`{2}` = `{3}`.`{4}`'.format(other_data['join'][0],
                                                                     tname,
                                                                     other_data['join'][1],
                                                                     other_data['join'][0],
                                                                     other_data['join'][2])

        return ''


    def _transform_return_data(self, data, tstruct, horizontal_key, other_data):

        if other_data and 'count' in other_data:
            return str(data[0]['count'])

        if not horizontal_key:
            return data

        ids = []
        for elem in data:
            ids.append(elem[horizontal_key])

        ids = list(set(ids))

        ret_data = []
        for id in ids:
            tmp = {horizontal_key : id}

            for elem in data:

                if elem[horizontal_key] != id:
                    continue

                if not elem['key'] in tmp:
                    tmp[elem['key']] = []
                tmp[elem['key']].append(elem['value'])

            ret_data.append(tmp)

        return ret_data