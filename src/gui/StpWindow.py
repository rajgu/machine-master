import curses
import logging
from src import Exec
from src import Job
from src import Stp
from src.db import DBAlarms
from src.db import DBStps
from src.db import DBJobs
from src.gui import Presenter
from src.gui import StpCommentsWindow
from src.gui import StpStatesWindow
from src.gui import UsersWindow
from src.gui import MessageBox
from src.helpers import KeysHelper
from lib.parsers import tgwParser
from lib.parsers import tgrParser
import src.gui.AlarmsWindow
import src.gui.JobsWindow
import src.gui.StpsWindow


class StpWindow:


    def __init__(self, db, screen, window, header, finder, footer, stpFindData):
        self.db          = db
        self.DBAlarms    = DBAlarms.DBAlarms(db)
        self.DBJobs      = DBJobs.DBJobs(db)
        self.Stp         = Stp.Stp(db)
        self.Job         = Job.Job(db)
        self.screen      = screen
        self.header      = header
        self.finder      = finder
        self.footer      = footer
        self.stpFindData = stpFindData
        self.window      = window
        self.msgBox      = MessageBox.MessageBox(screen, window, header)
        self.tgwParse    = tgwParser.tgwParser()
        self.tgrParse    = tgrParser.tgrParser()
        self.window.border(0)
        self.window.refresh()
        self.hardwareFields   = ['serial_number', 'location', 'type', 'name']


    def enter(self):
        action = self.presenter.getAction()
        if not action:
            return

        if action == 'showStpJobs':
            window = src.gui.JobsWindow.JobsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.stpData['name']})
        elif action == 'showStpAlarms':
            window = src.gui.AlarmsWindow.AlarmsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.stpData['name']})
        elif action == 'showStpComments':
            window = StpCommentsWindow.StpCommentsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.stpData['comments'])
        elif action == 'showStpStates':
            window = StpStatesWindow.StpStatesWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.stpData['states'])
        elif action == 'showStpOwners':
            window = UsersWindow.UsersWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.stpData['name']})
        elif action == 'showSiteStps':
            window = src.gui.StpsWindow.StpsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.stpData['site']})
        elif action == 'showOrgStps':
            window = src.gui.StpsWindow.StpsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.stpData['customer_organization']})
        elif action == 'showLink':
            _id = self.presenter.getSelected()
            window = Exec.Exec(self.dataToShow[_id]['value'])
        elif action == 'showTicket':
            _id = self.presenter.getSelected()
            window = Exec.Exec('{0}{1}'.format('https://plf-jira.rnd.ki.sw.ericsson.se/browse/', self.dataToShow[_id]['value']))
        elif action == 'showWorkerStps':
            window = src.gui.StpsWindow.StpsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {action: self.stpData['worker']})
        elif action == 'updateStpData':
            stpData = self.tgwParse.getStp(self.stpData['name'])
            stpData['site_lan_ip'] = self.stpData['site_lan_ip']
            self.Stp.save(stpData)
            jobsList = self.tgrParse.getJobs(self.stpData['name'], 100)
            jobsIds = map(lambda x: x['id'], jobsList)
            searchedJobs = self.DBJobs.read({'id' : jobsIds})
            searchedIds = map(lambda x: x['id'], searchedJobs)
            for job in jobsList:
                if int(job['id']) in searchedIds:
                    continue
                jobData = self.tgrParse.getJob(job['id'])
                self.Job.save(jobData)
            self.stpData = self.Stp.load(self.stpFindData)
            self._createPresenterData()
            self.presenter.updateData(self.dataToShow)
            self.msgBox.showInfo('Data for stp: {0} refreshed'.format(self.stpData['name']), 'Refresh data')
            self.presenter.refresh()
            return


        window.init()
        self.presenter.refresh()


    def init(self):

        self.stpData = self.Stp.load(self.stpFindData)
        self.header.addPosition('STP: {0}'.format(self.stpData['name']))

        self._createPresenterData()

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


    def _createPresenterData(self):
        jobs_cnt          = self.DBJobs.read({'stp': self.stpData['name']}, {'count': True})
        comments_cnt      = len(self.stpData['comments'])
        states_cnt        = len(self.stpData['states'])
        stp_state         = "Status: {0}, Locker: {1}".format(self.stpData['state']['status'], self.stpData['state']['locker'])
        self.owners = []
        for owner in self.stpData['owners']:
            self.owners.append({
                'signum': owner.keys()[0],
                'email' : owner.values()[0]
            })
        mapped_owners     = ", ".join(map(lambda x: x['signum'], self.owners))
        owners_cnt        = len(self.stpData['owners'])
        ala_cnt           = self.DBAlarms.read([['date_notice_end', 'IS', 'NULL'], ['stp_id', '=', self.stpData['id']]], {'count': True})
        ala_all_cnt       = self.DBAlarms.read({'stp_id': self.stpData['id']}, {'count': True})
        comment           = "show history comment" if self.stpData['comment'] == "" and len(self.stpData['comments']) > 0 else self.stpData['comment']

        self.dataToShow = [
            {'name': 'STP Name',                            'value': self.stpData['name'],                  'action': False},
            {'name': 'Last Data Update',                    'value': self.stpData['last_update'],           'action': 'updateStpData'},
            {'name': 'Site Lan IP',                         'value': self.stpData['site_lan_ip'],           'action': False},
            {'name': 'Active Alarms ({0})'.format(ala_cnt), 'value': 'show (all: {0})'.format(ala_all_cnt), 'action': 'showStpAlarms'},
            {'name': 'Jobs ({0})'.format(jobs_cnt),         'value': 'show',                                'action': 'showStpJobs'},
            {'name': 'Comments ({0})'.format(comments_cnt), 'value': comment,                               'action': 'showStpComments'},
            {'name': 'State ({0})'.format(states_cnt),      'value': stp_state,                             'action': 'showStpStates'},
            {'name': 'Owners ({0})'.format(owners_cnt),     'value': mapped_owners,                         'action': 'showStpOwners'},
            {'name': 'Organization',                        'value': self.stpData['customer_organization'], 'action': 'showOrgStps'},
            {'name': 'Ticket',                              'value': self.stpData['ticket'],                'action': 'showTicket'},
            {'name': 'Eris URL',                            'value': self.stpData['eris_url'],              'action': 'showLink'},
            {'name': 'Worker Log',                          'value': self.stpData['worker_log'],            'action': 'showLink'},
            {'name': 'Type',                                'value': self.stpData['type'],                  'action': False},
            {'name': 'Board Type',                          'value': self.stpData['board_type'],            'action': False},
            {'name': 'Duplex Type',                         'value': self.stpData['duplex_type'],           'action': False},
            {'name': 'Worker',                              'value': self.stpData['worker'],                'action': 'showWorkerStps'},
            {'name': 'Site',                                'value': self.stpData['site'],                  'action': 'showSiteStps'},
            {'name': 'Capacities',                          'spacer': True,                                 'action': False},
        ]
        if 'capacities' in self.stpData:
            for key, value in self.stpData['capacities'].iteritems():
                self.dataToShow.append({
                    'name':   key,
                    'value' : ", ".join(value),
                    'action': False
                })
        self.dataToShow.append(\
            {'name': 'Hardware',                            'spacer': True,                                 'action': False}
        )

        if 'hardware' in self.stpData:
            lengths = {}
            for field in self.hardwareFields:
                lengths[field] = 0

            for hardware in self.stpData['hardware']:
                for field in self.hardwareFields:
                    if field in hardware and len(hardware[field]) > lengths[field]:
                        lengths[field] = len(hardware[field])

            for hardware in self.stpData['hardware']:
                self.dataToShow.append({
                    'name':   '',
                    'value' : "{0}{1}  {2}{3}  {4}{5}  {6}{7}".format(
                        'SN: ',
                        hardware['serial_number'] + (lengths['serial_number'] - len(hardware['serial_number'])) * ' ',
                        'Location: ',
                        hardware['location'] + (lengths['location'] - len(hardware['location'])) * ' ',
                        'Type: ',
                        hardware['type'] + (lengths['type'] - len(hardware['type'])) * ' ',
                        'Name: ',
                        hardware['name'] + (lengths['name'] - len(hardware['name'])) * ' '
                    ),
                    'action': False
                })