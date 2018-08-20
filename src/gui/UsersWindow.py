import curses
import logging
from src.db import DBJobs
from src.db import DBUsers
from src.db import DBStpOwners
from src.db import DBStps
from src.gui import List
from src.gui import UserWindow
from src.helpers import Exporter
from src.helpers import KeysHelper


class UsersWindow:


    menuHeader = [
        ['Signum', 'signum'],
        ['Email',  'email'],
        ['Stps',   'stps'],
        ['Jobs',   'jobsCount']
    ]


    def __init__(self, db, screen, window, header, finder, footer, params=False):
        self.db          = db
        self.DBJobs      = DBJobs.DBJobs(db)
        self.DBUsers     = DBUsers.DBUsers(db)
        self.DBStpOwners = DBStpOwners.DBStpOwners(db)
        self.DBStps      = DBStps.DBStps(db)
        self.screen      = screen
        self.header      = header
        self.finder      = finder
        self.footer      = footer
        self.params      = params
        self.window      = window
        self.window.border(0)
        self.window.refresh()


    def enter(self):
        selected = self.list.getSelected()
        self.oldFilter = self.finder.getData()
        self.finder.clear()

        window = UserWindow.UserWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.usersList[selected]['signum'])
        window.init()

        self.finder.setData(self.oldFilter)
        self.list.refresh()
        self.window.refresh()


    def init(self):

        if self.params:
            if 'showStpOwners' in self.params:
                self.header.addPosition('Owners of STP: {0}'.format(self.params['showStpOwners']))

                stpId     = self.DBStps.read({'name': self.params['showStpOwners']}, {'fields': 'id'})[0]['id']
                owners    = self.DBStpOwners.read({'stp_id': stpId}, {'fields': 'user_id'})
                usersIds  = map(lambda x: x['user_id'], owners)
                usersList = self.DBUsers.read({'id': usersIds})
                stpOwners = self.DBStpOwners.read({'user_id': usersIds})

        else:
            self.header.addPosition('Users List')
            usersList = self.DBUsers.read({})
            stpOwners = self.DBStpOwners.read({})

        countedOwners = {}
        for stpOwner in stpOwners:
            if stpOwner['user_id'] in countedOwners:
                countedOwners[stpOwner['user_id']] += 1
            else:
                countedOwners[stpOwner['user_id']] = 1

        # Wyliczmy ile jobow przypada na poszczegolnego uzytkownika
        usersSignums   = map(lambda x: x['signum'], usersList)
        OwnerJobsCount = self.DBJobs.read({'owner': usersSignums}, {'fields': ['owner', 'COUNT(*) AS count'], 'groupBy': 'owner'})
        countedJobs    = {}
        for jobCnt in OwnerJobsCount:
            countedJobs[jobCnt['owner']] = jobCnt['count']

        self.usersList = []
        for user in usersList:
            if not user['signum']:
                continue

            self.usersList.append({
                'signum'   : user['signum'],
                'email'    : user['email'] if user['email'] else '-',
                'stps'     : countedOwners[user['id']] if user['id'] in countedOwners else 0,
                'jobsCount': countedJobs[user['signum']] if user['signum'] in countedJobs else 0
            })

        self.list = List.List(self.window, self.finder, self.usersList, self.menuHeader)
        self.list.refresh()

        keysHelper = KeysHelper.KeysHelper()
        exporter   = Exporter.Exporter(self.screen, self.window, self.header, self.menuHeader)

        while 1:
            key = self.screen.getch()

            if key not in keysHelper.getAll():
                continue

            if key in keysHelper.getEscape():
                break

            if key in keysHelper.getExport():
                exporter.jira(self.list.getFilteredData())
                self.list.refresh()

            if key in keysHelper.getNavigation():
                self.list.input(key)

            if key in keysHelper.getInput():
                self.finder.input(key)
                self.list.refresh()

            if key in keysHelper.getEnter():
                self.enter()

        self.header.removePosition()
        self.finder.clear()
