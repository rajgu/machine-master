import curses
import logging
from src.db import DBJobs
from src.db import DBUsers
from src.db import DBStps
from src.db import DBStpOwners
from src.gui import Presenter
from src.helpers import KeysHelper
import src.gui.StpsWindow
import src.gui.JobsWindow


class UserWindow:


    def __init__(self, db, screen, window, header, finder, footer, userSignum):
        self.db          = db
        self.DBJobs      = DBJobs.DBJobs(db)
        self.DBUsers     = DBUsers.DBUsers(db)
        self.DBStps      = DBStps.DBStps(db)
        self.DBStpOwners = DBStpOwners.DBStpOwners(db)
        self.screen      = screen
        self.header      = header
        self.finder      = finder
        self.footer      = footer
        self.window      = window
        self.userSignum  = userSignum
        self.window.border(0)
        self.window.refresh()


    def enter(self):

        action = self.presenter.getAction()
        if not action:
            return

        if action == 'showUserStps':
            window = src.gui.StpsWindow.StpsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.userSignum})
        elif action == 'showUserJobs':
            window = src.gui.JobsWindow.JobsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.userSignum})

        window.init()
        self.presenter.refresh()


    def init(self):

        self.header.addPosition("User: {0}".format(self.userSignum))
        userData = self.DBUsers.read({'signum': self.userSignum})
        userStpsCount = len(self.DBStpOwners.read({'user_id': userData[0]['id']}))
        userJobsCount = self.DBJobs.read({'owner' : self.userSignum}, {'count': True})

        self.dataToShow = [
            {'name' : 'Signum',                           'value': userData[0]['signum'], 'action': False,          'scroll': False},
            {'name' : 'Email',                            'value': userData[0]['email'],  'action': False,          'scroll': False},
            {'name' : 'Stps ({0})'.format(userStpsCount), 'value': "show",                'action': 'showUserStps', 'scroll': True},
            {'name' : 'Jobs ({0})'.format(userJobsCount), 'value': "show",                'action': 'showUserJobs', 'scroll': True}
        ]

        self.presenter = Presenter.Presenter(self.window, self.dataToShow)
        self.presenter.refresh()

        keysHelper = KeysHelper.KeysHelper()
        while 1:
            key = self.screen.getch()

            if key not in keysHelper.getAll():
                continue

            if key in keysHelper.getEscape():
                break

            if key in keysHelper.getNavigation():
                self.presenter.input(key)

            if key in keysHelper.getEnter():
                self.enter()

        self.header.removePosition()
        self.finder.clear()
