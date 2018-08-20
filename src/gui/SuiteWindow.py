import curses
import logging
from src.db import DBJobs
from src.db import DBJobsSuites
from src.gui import Presenter
from src.helpers import KeysHelper
import src.gui.JobsWindow


class SuiteWindow:


    def __init__(self, db, screen, window, header, finder, footer, suiteName):
        self.db           = db
        self.DBJobs       = DBJobs.DBJobs(db)
        self.DBJobsSuites = DBJobsSuites.DBJobsSuites(db)
        self.screen       = screen
        self.header       = header
        self.finder       = finder
        self.footer       = footer
        self.window       = window
        self.suiteName    = suiteName
        self.window.border(0)
        self.window.refresh()


    def enter(self):

        action = self.presenter.getAction()

        if not action:
            return

        if action == 'showSuiteJobs':
            window = src.gui.JobsWindow.JobsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.suiteName})

        window.init()
        self.presenter.refresh()


    def init(self):

        self.header.addPosition("Suite: {0}".format(self.suiteName))
        suitesIds      = self.DBJobsSuites.read({'suite' : self.suiteName}, {'fields': 'job_id'})
        suiteJobsCount = len(suitesIds)
        suiteJobsIds   = map(lambda x: x['job_id'], suitesIds)
        oldestJob      = self.DBJobs.read({'id' : suiteJobsIds}, {'order': 'date_created', 'sort': 'ASC', 'limit' : 1})
        newestJob      = self.DBJobs.read({'id' : suiteJobsIds}, {'order': 'date_created', 'sort': 'DESC', 'limit' : 1})

        self.dataToShow = [
            {'name' : 'Suite',                             'value': self.suiteName,               'action': False},
            {'name' : 'Oldest Job',                        'value': oldestJob[0]['date_created'], 'action': False},
            {'name' : 'Newest Job',                        'value': newestJob[0]['date_created'], 'action': False},
            {'name' : 'Jobs ({0})'.format(suiteJobsCount), 'value': 'show',                       'action': 'showSuiteJobs'}
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
