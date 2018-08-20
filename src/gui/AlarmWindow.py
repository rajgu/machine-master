import curses
import logging
from src.db import DBAlarms
from src.db import DBStps
from src.gui import Presenter
from src.helpers import KeysHelper
import src.gui.StpWindow


class AlarmWindow:


    def __init__(self, db, screen, window, header, finder, footer, alarmId):
        self.db       = db
        self.DBAlarms = DBAlarms.DBAlarms(db)
        self.DBStps   = DBStps.DBStps(db)
        self.screen   = screen
        self.header   = header
        self.finder   = finder
        self.footer   = footer
        self.alarmId  = alarmId
        self.window   = window
        self.window.border(0)
        self.window.refresh()


    def enter(self):
        action = self.presenter.getAction()
        if not action:
            return

        if action == 'showStp':
            window = src.gui.StpWindow.StpWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.stpData[0])

        window.init()
        self.window.refresh()


    def init(self):

        alarmData    = self.DBAlarms.read({'id': self.alarmId})
        self.stpData = self.DBStps.read({'id': alarmData[0]['stp_id']})

        self.header.addPosition('Alarm Details ({0})'.format(alarmData[0]['id']))

        self.dataToShow = [
            {'name': 'Inner Id',                'value': alarmData[0]['id'],                      'action': False},
            {'name': 'Stp',                     'value': self.stpData[0]['name'],                 'action': 'showStp'},
            {'name': 'Date Notice Start',       'value': alarmData[0]['date_notice_start'],       'action': False},
            {'name': 'Date Notice End',         'value': alarmData[0]['date_notice_end'],         'action': False},
            {'name': 'Alarm Data',              'spacer': True},
            {'name': 'alarm_id',                'value': alarmData[0]['alarm_id'],                'action': False},
            {'name': 'Event Time',              'value': alarmData[0]['event_time'],              'action': False},
            {'name': 'Perceived Severity',      'value': alarmData[0]['perceived_severity'],      'action': False},
            {'name': 'Managed Object Class',    'value': alarmData[0]['managed_object_class'],    'action': False},
            {'name': 'Managed Object Instance', 'value': alarmData[0]['managed_object_instance'], 'action': False},
            {'name': 'Specific Problem',        'value': alarmData[0]['specific_problem'],        'action': False},
            {'name': 'Probable Cause',          'value': alarmData[0]['probable_cause'],          'action': False},
            {'name': 'Additional Text',         'value': alarmData[0]['additional_text'],         'action': False},
            {'name': 'Acknowledged By',         'value': alarmData[0]['acknowledged_by'],         'action': False},
            {'name': 'Acknowledgement Time',    'value': alarmData[0]['acknowledgement_time'],    'action': False},
            {'name': 'Acknowledgement State',   'value': alarmData[0]['acknowledgement_state'],   'action': False},
            {'name': 'System Dn',               'value': alarmData[0]['system_dn'],               'action': False},
            {'name': 'Notification Id',         'value': alarmData[0]['notification_id'],         'action': False},
            {'name': 'Additional Info',         'value': alarmData[0]['additional_info'],         'action': False},
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

            if key in keysHelper.getEnter():
                self.enter()

            if key in keysHelper.getNavigation():
                self.presenter.input(key)

        self.header.removePosition()
        self.finder.clear()
