import curses
import logging
from src import Exec
from src import Job
from src.gui import Presenter
from src.helpers import KeysHelper
import src.gui.UPWindow
import src.gui.UserWindow
import src.gui.StpWindow
import src.gui.SuiteWindow


class JobWindow:


    def __init__(self, db, screen, window, header, finder, footer, jobFindData):
        self.db               = db
        self.Job              = Job.Job(db)
        self.screen           = screen
        self.header           = header
        self.finder           = finder
        self.footer           = footer
        self.jobFindData      = jobFindData
        self.window           = window
        self.window.border(0)
        self.window.refresh()


    def enter(self):
        action = self.presenter.getAction()
        if not action:
            return

        if action == 'showJobUp':
            window = src.gui.UPWindow.UPWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {'name': self.jobData['up']})
        elif action == 'showPropUp':
            window = src.gui.UPWindow.UPWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {'name': self.jobData['prop_up']})
        elif action == 'showPropOwner':
            window = src.gui.UserWindow.UserWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.jobData['owner'])
        elif action == 'showPropStp':
            window = src.gui.StpWindow.StpWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {'name': self.jobData['stp']})
        elif action == 'showPropUStp':
            window = src.gui.StpWindow.StpWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, {'name': self.jobData['use_stp']})
        elif action == 'showSuite':
            _id = self.presenter.getSelected()
            window = src.gui.SuiteWindow.SuiteWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.dataToShow[_id]['_suite'])
        elif action == 'showLink':
            _id = self.presenter.getSelected()
            window = Exec.Exec(self.dataToShow[_id]['value'])

        window.init()
        self.presenter.refresh()


    def init(self):

        self.jobData = self.Job.load(self.jobFindData)
        self.header.addPosition('JOB: {0}'.format(self.jobData['id']))

        self.dataToShow = [
            {'name': 'JOB ID',                'value': self.jobData['id'],                              'action': False},
            {'name': 'Digital Unit',          'value': self.jobData['du'],                              'action': False},
            {'name': 'Type',                  'value': self.jobData['type'],                            'action': False},
            {'name': 'Duplex',                'value': self.jobData['duplex'],                          'action': False},
            {'name': 'Installation Type',     'value': self.jobData['inst_type'],                       'action': False},
            {'name': 'UP',                    'value': self.jobData['up'],                              'action': 'showJobUp'},
            {'name': 'Event',                 'value': self.jobData['event'],                           'action': False},
            {'name': 'Date & Times',          'spacer': True,                                           'action': False},
            {'name': 'Date Created',          'value': self.jobData['date_created'],                    'action': False},
            {'name': 'Date RCM Install',      'value': self.jobData['date_rcm_install'],                'action': False},
            {'name': 'Date Started',          'value': self.jobData['date_started'],                    'action': False},
            {'name': 'Date Finished',         'value': self.jobData['date_finished'],                   'action': False},
            {'name': 'Time Preparation',      'value': "{0}m".format(self.jobData['time_prep']),        'action': False},
            {'name': 'Time Test',             'value': "{0}m".format(self.jobData['time_test']),        'action': False},
            {'name': 'Time Utilization',      'value': "{0}m".format(self.jobData['time_utilization']), 'action': False},
            {'name': 'Properties',            'spacer': True,                                           'action': False},
            {'name': 'Force Install',         'value': self.jobData['force_install'],                   'action': False},
            {'name': 'UP',                    'value': self.jobData['prop_up'],                         'action': 'showPropUp'},
            {'name': 'Priority',              'value': self.jobData['priority'],                        'action': False},
            {'name': 'Owner',                 'value': self.jobData['owner'],                           'action': 'showPropOwner'},
            {'name': 'STP',                   'value': self.jobData['stp'],                             'action': 'showPropStp'},
            {'name': 'Criteria',              'value': self.jobData['criteria'],                        'action': False},
            {'name': 'IP Version',            'value': self.jobData['ip_version'],                      'action': False},
            {'name': 'Use STP',               'value': self.jobData['use_stp'],                         'action': 'showPropUStp'},
            {'name': 'Suites (ok/nok/skip)',  'spacer': True,                                           'action': False}
        ]
        if 'suites' in self.jobData:
            suiteLength = 0
            for suite in self.jobData['suites']:
                if len(suite['suite']) > suiteLength:
                    suiteLength = len(suite['suite'])

            if suiteLength > 0:
                for suite in self.jobData['suites']:
                    self.dataToShow.append({
                        'name':   '',
                        'value' : "{0} {1}{2}{3}{4}{5}{6}".format(
                            suite['suite'],
                            ' ' * (suiteLength - len(suite['suite']) + (3 - len(str(suite['ok'])))),
                            suite['ok'],
                            ' ' * (3 - len(str(suite['nok']))),
                            suite['nok'],
                            ' ' * (3 - len(str(suite['skip']))),
                            suite['skip']
                        ),
                        'action': 'showSuite',
                        '_suite': suite['suite']
                    })
        self.dataToShow.append(
            {'name': 'Target',                'spacer': True,                            'action': False}
        )
        if 'job_targets' in self.jobData:
            for key, value in self.jobData['job_targets'].iteritems():
                self.dataToShow.append({
                    'name':   key,
                    'value':  ", ".join(value),
                    'action': False
                })
        self.dataToShow.append(
            {'name': 'Tool Versions',         'spacer': True,                            'action': False}
        )
        if 'tool_versions' in self.jobData:
            for key, value in self.jobData['tool_versions'].iteritems():
                self.dataToShow.append({
                    'name':   key,
                    'value':  ", ".join(value),
                    'action': False
                })
        self.dataToShow.append(
            {'name': 'Links',                 'spacer': True,                            'action': False}
        )
        if 'job_links' in self.jobData:
            # Zahardkodowany link do DTjob, jezeli ten istnieje:
            if 'basedir' in self.jobData['job_links']:
                self.dataToShow.append({
                    'name':   'DT Job',
                    'value':  '{0}/dtjob.txt'.format(self.jobData['job_links']['basedir'][0]),
                    'action': 'showLink'
                })

            for key, value in self.jobData['job_links'].iteritems():
                if isinstance(value, list):
                    for link in value:
                        self.dataToShow.append({
                            'name':   key,
                            'value':  link,
                            'action': 'showLink'
                        })
                else:
                    self.dataToShow.append({
                        'name':   key,
                        'value':  value,
                        'action': 'showLink'
                    })

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
