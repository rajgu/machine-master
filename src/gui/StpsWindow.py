import curses
import logging
from src.db import DBStps
from src.db import DBUsers
from src.db import DBStpOwners
from src.gui import List
from src.helpers import Exporter
from src.helpers import KeysHelper
import src.gui.StpWindow


class StpsWindow:


    menuHeader = [
        ['Name',         'name'],
        ['Duplex',       'duplex_type'],
        ['Organization', 'customer_organization'],
        ['Worker',       'worker'],
        ['Site',         'site'],
        ['Board',        'board_type'],
        ['Type',         'type'],
        ['Status',       'status'],
    ]


    def __init__(self, db, screen, window, header, finder, footer, params = False):
        self.db          = db
        self.DBStps      = DBStps.DBStps(self.db)
        self.DBUsers     = DBUsers.DBUsers(self.db)
        self.DBStpOwners = DBStpOwners.DBStpOwners(self.db)
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

        if selected == type(False):
            return

        window = src.gui.StpWindow.StpWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.stpsList[selected])

        window.init()
        self.finder.setData(self.oldFilter)
        self.list.refresh()
        self.window.refresh()


    def init(self):

        if self.params:
            if 'showUserStps' in self.params:
                self.header.addPosition('STPs of user: {0}'.format(self.params['showUserStps']))

                userData = self.DBUsers.read({'signum': self.params['showUserStps']})
                userStpsList = self.DBStpOwners.read({'user_id': userData[0]['id']})
                userStpsIds = map(lambda x: x['stp_id'], userStpsList)

                self.stpsList = self.DBStps.read({'id': userStpsIds});

            elif 'showOrgStps' in self.params:
                self.header.addPosition('STPs of org: {0}'.format(self.params['showOrgStps']))
                self.stpsList = self.DBStps.read({'customer_organization': self.params['showOrgStps']})

            elif 'showWorkerStps' in self.params:
                self.header.addPosition('STPs of worker: {0}'.format(self.params['showWorkerStps']))
                self.stpsList = self.DBStps.read({'worker': self.params['showWorkerStps']})

            elif 'showSiteStps' in self.params:
                self.header.addPosition('STPs from Site: {0}'.format(self.params['showSiteStps']))
                self.stpsList = self.DBStps.read({'site': self.params['showSiteStps']})

        else:
            self.header.addPosition('STPs List')
            self.stpsList = self.DBStps.read({});

        self.list = List.List(self.window, self.finder, self.stpsList, self.menuHeader)
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
