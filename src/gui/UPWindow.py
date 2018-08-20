from __future__ import division
import curses
import logging
from src.db import DBJobs
from src.gui import Presenter
from src.helpers import KeysHelper
from src.helpers import DateHelper
import src.gui.JobsWindow


class UPWindow:


    def __init__(self, db, screen, window, header, finder, footer, upFindData):
        self.db          = db
        self.DBJobs      = DBJobs.DBJobs(db)
        self.screen      = screen
        self.header      = header
        self.finder      = finder
        self.footer      = footer
        self.window      = window
        self.upFindData  = upFindData
        self.dateHelper  = DateHelper.DateHelper()
        self.window.border(0)
        self.window.refresh()


    def enter(self):

        action = self.presenter.getAction()
        logging.fatal(action)
        if not action:
            return

        if action == 'showUpJobs':
            window = src.gui.JobsWindow.JobsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.upFindData['name']})

        window.init()
        self.presenter.refresh()


    def init(self):

        self.header.addPosition("UP: {0}".format(self.upFindData['name']))

        upJobs    = self.DBJobs.read({'up' : self.upFindData['name']}, {'order': 'date_created', 'sort': 'ASC'})
        jobs24h   = self.DBJobs.read([['up', '=', self.upFindData['name']], ['date_created', '>=', self.dateHelper.getDateTimeDelta(-1)]])
        jobs7d    = self.DBJobs.read([['up', '=', self.upFindData['name']], ['date_created', '>=', self.dateHelper.getDateTimeDelta(-7)]])
        jobsCount = len(upJobs)
        oldestJob = upJobs[0]
        newestJob = upJobs[-1]

        self.dataToShow = [
            {'name' : 'Name',                           'value': self.upFindData['name'],   'action': False},
            {'name' : 'Oldest Job',                     'value': oldestJob['date_created'], 'action': False},
            {'name' : 'Newest Job',                     'value': newestJob['date_created'], 'action': False},
            {'name' : 'Jobs ({0})'.format(len(upJobs)), 'value': 'show',                    'action': 'showUpJobs'}
        ]

        if len(jobs24h) > 0:
            self.dataToShow.append({'name' : 'Last 24 hours ({0})'.format(len(jobs24h)), 'spacer': True})
            self._calculateUpEvents(jobs24h)
        if len(jobs7d) > 0:
            self.dataToShow.append({'name' : 'Last 7 days ({0})'.format(len(jobs7d)),    'spacer': True})
            self._calculateUpEvents(jobs7d)
        self.dataToShow.append({'name' : 'All Time ({0})'.format(len(upJobs)),           'spacer': True})
        self._calculateUpEvents(upJobs)

        self.dataToShow.append({'name' : 'Executions By STP',                            'spacer': True})
        execByStp = {}
        for job in upJobs:
            if not job['stp'] in execByStp:
                execByStp[job['stp']] = 1
            else:
                execByStp[job['stp']] += 1

        for stpName, count in execByStp.iteritems():
            percent = round(count * 100 / jobsCount, 2)
            self.dataToShow.append({'name': stpName, 'value': '{0}{1}{2}%'.format(
                count, ' ' * (4 - len(str(count))), percent), 'action': False})

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


    def _calculateUpEvents(self, data):
        jobsCount = len(data)
        events    = {'OK': 0}
        for job in data:
            if job['event'] == '':
                events['OK'] += 1
                continue
            if job['event'] in events:
                events[job['event']] += 1
            else:
                events[job['event']] = 1
        for name, count in events.iteritems():
            percent = round(count * 100 / jobsCount, 2)
            value = '{0}{1}{2}{3}%'.format(
                ' ' * (3 - len(str(count))),
                count,
                ' ' * (4 - len(str(count))), percent
            )
            self.dataToShow.append({'name': name, 'value': value, 'action': False})
