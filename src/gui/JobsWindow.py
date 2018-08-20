import curses
import logging
from src.db import DBJobs
from src.db import DBJobsSuites
from src.gui import List
from src.gui import JobWindow
from src.helpers import Exporter
from src.helpers import KeysHelper
import src.gui.StpWindow


class JobsWindow:


    menuHeader = [
        ['Id',      'id'],
        ['Created', 'date_created'],
        ['Event',   'event'],
        ['Suite',   'suite'],
        ['Ok',      'ok'],
        ['Nok',     'nok'],
        ['Skip',    'skip'],
        ['Duplex',  'duplex'],
        ['UP',      'up'],
        ['Owner',   'owner'],
        ['STP',     'stp']
    ]


    def __init__(self, db, screen, window, header, finder, footer, params=False):
        self.db           = db
        self.DBJobs       = DBJobs.DBJobs(self.db)
        self.DBJobsSuites = DBJobsSuites.DBJobsSuites(self.db)
        self.screen       = screen
        self.header       = header
        self.finder       = finder
        self.footer       = footer
        self.params       = params
        self.window       = window
        self.window.border(0)
        self.window.refresh()


    def enter(self):
        self.oldFilter = self.finder.getData()
        self.finder.clear()
        selected = self.list.getSelected()

        if selected == type(False):
            return False

        window = JobWindow.JobWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.jobsList[selected])

        window.init()
        self.finder.setData(self.oldFilter)
        self.list.refresh()
        self.window.refresh()


    def init(self):

        if self.params:
            if 'showUpJobs' in self.params:
                self.header.addPosition('Jobs for UP: {0}'.format(self.params['showUpJobs']))
                jobsList = self.DBJobs.read({'up' : self.params['showUpJobs']}, {'sort': 'DESC','order': 'id'});

            elif 'showStpJobs' in self.params:
                self.header.addPosition('Jobs for STP: {0}'.format(self.params['showStpJobs']))
                jobsList = self.DBJobs.read({'stp': self.params['showStpJobs']}, {'sort': 'DESC','order': 'id'})

            elif 'showUserJobs' in self.params:
                self.header.addPosition('Jobs for User: {0}'.format(self.params['showUserJobs']))
                jobsList = self.DBJobs.read({'owner' : self.params['showUserJobs']}, {'sort': 'DESC','order': 'id'})

            elif 'showSuiteJobs' in self.params:
                self.header.addPosition('Jobs for Suite: {0}'.format(self.params['showSuiteJobs']))
                suitesIds    = self.DBJobsSuites.read({'suite' : self.params['showSuiteJobs']}, {'fields': 'job_id'})
                suiteJobsIds = map(lambda x: x['job_id'], suitesIds)
                jobsList     = self.DBJobs.read({'id' : suiteJobsIds}, {'sort': 'DESC','order': 'id'})

        else:
            self.header.addPosition('Jobs List')
            jobsList = self.DBJobs.read({}, {'sort': 'DESC','order': 'id', 'limit': 10000});

        jobsIds = map(lambda x: x['id'], jobsList)
        jobsSuites = self.DBJobsSuites.read({'job_id' : jobsIds})
        mappedSuites = {}
        for prop in jobsSuites:
            tmpJobId = prop['job_id']
            del(prop['job_id'])
            if tmpJobId in mappedSuites:
                mappedSuites[tmpJobId].append(prop)
            else:
                mappedSuites[tmpJobId] = [prop]

        self.jobsList = []
        for job in jobsList:
            job['suite'] = map(lambda x: x['suite'], mappedSuites[job['id']])
            job['ok']    = map(lambda x: x['ok'], mappedSuites[job['id']])
            job['nok']   = map(lambda x: x['nok'], mappedSuites[job['id']])
            job['skip']  = map(lambda x: x['skip'], mappedSuites[job['id']])
            self.jobsList.append(job)

        self.list = List.List(self.window, self.finder, self.jobsList, self.menuHeader)
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
