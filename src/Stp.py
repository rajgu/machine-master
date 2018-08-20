#!/usr/bin/env python2
import logging

from src.db.DBStps import DBStps
from src.db.DBStpCapacities import DBStpCapacities
from src.db.DBStpComments import DBStpComments
from src.db.DBStpHardware import DBStpHardware
from src.db.DBStpMisc import DBStpMisc
from src.db.DBStpOwners import DBStpOwners
from src.db.DBUsers import DBUsers
from src.db.DBStpStatesHistory import DBStpStatesHistory
from src.helpers.DateHelper import DateHelper

class Stp:

    def __init__(self, db):
        self.db                 = db
        self.DBStps             = DBStps(db)
        self.DBStpCapacities    = DBStpCapacities(db)
        self.DBStpComments      = DBStpComments(db)
        self.DBStpHardware      = DBStpHardware(db)
        self.DBStpMisc          = DBStpMisc(db)
        self.DBUsers            = DBUsers(db)
        self.DBStpOwners        = DBStpOwners(db)
        self.DBStpStatesHistory = DBStpStatesHistory(db)
        self.DateHelper         = DateHelper()



    def save(self, stpData):

        if not stpData:
            raise Exception ("No stp Data to save")
        if not stpData['name']:
            raise Exception ("Trying to save nameless STP")

        oldCommit = self.db.getAutocommit()
        self.db.setAutocommit(False)

        existingStp = self.DBStps.read({'name' : stpData['name']})

        if existingStp:
            stpId = existingStp[0]['id']
            self.DBStpCapacities.delete({'stp_id' : stpId})
            self.DBStpHardware.delete({'stp_id' : stpId})
            self.DBStpMisc.delete({'stp_id' : stpId})
            self.DBStpOwners.delete({'stp_id' : stpId})

            self.DBStps.update({
                'name':                  stpData['name'].strip(),
                'board_type':            stpData['board_type'].strip(),
                'duplex_type':           stpData['duplex_type'].lower().strip(),
                'site':                  stpData['site'].strip(),
                'worker':                stpData['worker'].strip(),
                'customer_organization': stpData['customer_organization'].strip() if 'customer_organization' in stpData else '',
                'eris_url':              stpData['eris_url'].strip() if 'eris_url' in stpData else '',
                'worker_log':            stpData['worker_log'].strip() if 'worker_log' in stpData else '',
                'type':                  stpData['type'].strip(),
                'last_update':           self.DateHelper.getCurrentDateTime(),
                'site_lan_ip':           stpData['site_lan_ip'].strip() if 'site_lan_ip' in stpData else '',
                'status':                stpData['state']['status'].strip() if 'state' in stpData else '',
            }, {'id' : stpId})

        else:
            self.DBStps.create({
                'name':                  stpData['name'].strip(),
                'board_type':            stpData['board_type'].strip(),
                'duplex_type':           stpData['duplex_type'].lower().strip(),
                'site':                  stpData['site'].strip(),
                'worker':                stpData['worker'].strip(),
                'customer_organization': stpData['customer_organization'].strip() if 'customer_organization' in stpData else '',
                'eris_url':              stpData['eris_url'].strip() if 'eris_url' in stpData else '',
                'worker_log':            stpData['worker_log'].strip() if 'worker_log' in stpData else '',
                'type':                  stpData['type'].strip(),
                'last_update':           self.DateHelper.getCurrentDateTime(),
                'site_lan_ip':           stpData['site_lan_ip'].strip() if 'site_lan_ip' in stpData else '',
                'status':                stpData['state']['status'].strip() if 'state' in stpData else '',
            })
            savedStp = self.DBStps.read({'name' : stpData['name']})
            stpId = savedStp[0]['id']

        capacities = stpData['capacities']
        capacities['stp_id'] = stpId
        self.DBStpCapacities.create(capacities)

        if 'comment' in stpData:

            newestComment = self.DBStpComments.read({'stp_id' : stpId}, {'order' : 'id', 'sort' : 'DESC', 'limit' : 1})
            if not newestComment or newestComment[0]['text'] != stpData['comment']:
                self.DBStpComments.create({
                    'stp_id' : stpId,
                    'text' : stpData['comment'],
                    'ticket' : stpData['ticket'],
                    'date' : self.DateHelper.getCurrentDateTime()
                })

        if 'hardware' in stpData and stpData['hardware']:
            hardwareToAdd = []
            for hardware in stpData['hardware']:
                tmpHardware = hardware
                tmpHardware['stp_id'] = stpId
                hardwareToAdd.append(tmpHardware)
            self.DBStpHardware.create(hardwareToAdd)

        if 'misc' in stpData and stpData['misc']:
            misc = stpData['misc']
            misc['stp_id'] = stpId
            self.DBStpMisc.create(misc)

        owners = map(lambda x: x[0], stpData['owners'].iteritems())
        searchedOwners = self.DBUsers.read({'signum': owners})

        for user in  searchedOwners:
            if not user['email']:
                self.DBUsers.update({'email' : stpData['owners'][user['signum']]}, {'signum' : user['signum']})

        searchedFiltered = map(lambda x: x['signum'], searchedOwners)
        usersToAdd = []

        if len(searchedFiltered) > 0:
            for signum, mail in stpData['owners'].iteritems():
                if not signum in searchedFiltered:
                    usersToAdd.append({'signum' : signum, 'email' : mail})
        else:
            usersToAdd = map(lambda x: {'signum' : x[0], 'email' : x[1]}, stpData['owners'].iteritems())

        if len(usersToAdd) > 0:
            self.DBUsers.create(usersToAdd)

        ownersInsert = []
        allOwners = self.DBUsers.read({'signum': owners})
        for owner in allOwners:
            ownersInsert.append({'stp_id' : stpId, 'user_id' : owner['id']})
        if ownersInsert:
            self.DBStpOwners.create(ownersInsert)

        searchedLocker = self.DBUsers.read({'signum' : stpData['state']['locker']})
        if not searchedLocker:
            self.DBUsers.create({'signum' : stpData['state']['locker']})
            searchedLocker = self.DBUsers.read({'signum' : stpData['state']['locker']})

        newestState = self.DBStpStatesHistory.read({'stp_id' : stpId}, {'order' : 'id', 'sort' : 'DESC', 'limit' : 1})

        if not newestState or newestState[0]['new_state'] != stpData['state']['status'] or newestState[0]['locker_id'] != searchedLocker[0]['id']:
            self.DBStpStatesHistory.create({
                'stp_id' : stpId,
                'new_state' : stpData['state']['status'],
                'locker_id' : searchedLocker[0]['id'],
                'date' : self.DateHelper.getCurrentDateTime()
            })

        if oldCommit:
            self.db.commit()

        self.db.setAutocommit(oldCommit)



    def load(self, stpSearchData):

        stpData = False
        if 'name' in stpSearchData:
            stpData = self.DBStps.read({'name' : stpSearchData['name']})

        if not stpData:
            return False

        stpData = stpData[0]

        capacities = self.DBStpCapacities.read({'stp_id' : stpData['id']})
        del capacities[0]['stp_id']
        stpData['capacities'] = capacities[0]

        comments = self.DBStpComments.read({'stp_id' : stpData['id']}, {'sort' : 'DESC', 'order' : 'id'})
        if len(comments) > 0:
            stpData['comment'] = comments[0]['text']
            stpData['ticket']  = comments[0]['ticket']
        else:
            stpData['comment'] = ''
            stpData['ticket']  = ''
        stpData['comments'] = []
        for comment in comments:
            del comment['id']
            del comment['stp_id']
            stpData['comments'].append(comment)

        hardware = self.DBStpHardware.read({'stp_id' : stpData['id']})
        stpData['hardware'] = []
        for hard in hardware:
            del hard['stp_id']
            stpData['hardware'].append(hard)

        misc = self.DBStpMisc.read({'stp_id' : stpData['id']})
        if misc:
            del misc[0]['stp_id']
            stpData['misc'] = misc[0]
        else:
            stpData['misc'] = ''

        owners = self.DBStpOwners.read({'stp_id' : stpData['id']})
        ownersIds = map(lambda x: x['user_id'], owners)
        users = self.DBUsers.read({'id' : ownersIds})
        stpData['owners'] = []
        for user in users:
            stpData['owners'].append({user['signum'] : user['email']})

        states = self.DBStpStatesHistory.read({'stp_id' : stpData['id']}, {'sort' : 'DESC', 'order' : 'id'})
        if states[0]['locker_id']:
            locker = self.DBUsers.read({'id' : states[0]['locker_id']})[0]['signum']
        else:
            locker = ''
        stpData['state'] = {}
        stpData['state']['status'] = states[0]['new_state']
        stpData['state']['locker'] = locker
        stpData['states'] = []
        for state in states:
            if state['locker_id']:
                locker = self.DBUsers.read({'id' : state['locker_id']})[0]['signum']
            else:
                locker = ''
            stpData['states'].append({'status' : state['new_state'], 'locker' : locker, 'date' : state['date']})

        return stpData



    def remove(self, stpSearchData):
        if 'name' in stpSearchData:
            stpData = self.DBStps.read({'name' : stpSearchData['name']})

        if not stpData:
            raise Exception("Could not find stp to deletion, search data: {0}".format(stpSearchData))

        oldCommit = self.db.getAutocommit()
        self.db.setAutocommit(False)

        stpId = stpData[0]['id']

        self.DBStps.delete({'id' : stpId})
        self.DBStpCapacities.delete({'stp_id' : stpId})
        self.DBStpComments.delete({'stp_id' : stpId})
        self.DBStpHardware.delete({'stp_id' : stpId})
        self.DBStpMisc.delete({'stp_id' : stpId})
        self.DBStpOwners.delete({'stp_id' : stpId})
        self.DBStpStatesHistory.delete({'stp_id' : stpId})

        if oldCommit:
            self.db.commit()

        self.db.setAutocommit(oldCommit)

