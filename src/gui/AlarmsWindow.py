import curses
import logging
from src.db import DBAlarms
from src.db import DBStps
from src.gui import List
from src.gui import AlarmWindow
from src.helpers import Exporter
from src.helpers import KeysHelper


class AlarmsWindow:


    menuHeader = [
        ['Active',           'active'],
        ['Specific Problem', 'specific_problem'],
        ['Severity',         'perceived_severity'],
        ['Probable Cause',   'probable_cause'],
        ['Stp Name',         'stp_name'],
        ['Date Noticed',     'date_notice_start'],
        ['Additional Text',  'additional_text']
    ]


    def __init__(self, db, screen, window, header, finder, footer, params = False):
        self.db       = db
        self.DBAlarms = DBAlarms.DBAlarms(db)
        self.DBStps   = DBStps.DBStps(db)
        self.screen   = screen
        self.header   = header
        self.finder   = finder
        self.footer   = footer
        self.window   = window
        self.params   = params
        self.window.border(0)
        self.window.refresh()


    def enter(self):
        selected = self.list.getSelected()
        self.oldFilter = self.finder.getData()
        self.finder.clear()

        window = AlarmWindow.AlarmWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.alarmsList[selected]['id'])
        window.init()

        self.finder.setData(self.oldFilter)
        self.list.refresh()
        self.window.refresh()


    def init(self):

        if self.params:
            if 'showStpAlarms' in self.params:
                self.header.addPosition('Alarms of STP: {0}'.format(self.params['showStpAlarms']))
                stpData = self.DBStps.read({'name': self.params['showStpAlarms']})
                alarmList = self.DBAlarms.read({'stp_id': stpData[0]['id']}, {'sort': 'DESC','order': 'id'})
        else:
            self.header.addPosition('Active Alarms List')
            alarmList = self.DBAlarms.read([['date_notice_end', 'IS', 'NULL']])

        stpIds  = map(lambda x: x['stp_id'], alarmList)
        stpData = self.DBStps.read({'id': stpIds})
        stpMap  = {}
        for stp in stpData:
            stpMap[stp['id']] = stp['name']

        self.alarmsList = []
        for alarm in alarmList:
            alarm['stp_name'] = stpMap[alarm['stp_id']]
            alarm['active']   = 'YES' if alarm['date_notice_end'] == None else 'NO'
            self.alarmsList.append(alarm)

        self.list = List.List(self.window, self.finder, self.alarmsList, self.menuHeader)
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
