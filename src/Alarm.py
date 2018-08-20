#!/usr/bin/env python2
import logging

from src.db.DBAlarms import DBAlarms
from src.db.DBStps import DBStps
from src.helpers.DateHelper import DateHelper


class Alarm:


    _alarm_cmp_fields = [
        'alarm_id',
        'event_time',
        'perceived_severity',
        'managed_object_class',
        'managed_object_instance',
        'specific_problem',
        'failure_problem_cause',
        'additional_text',
        'acknowledged_by',
        'acknowledgement_time',
        'acknowledgement_state',
        'system_dn',
        'notification_id',
        'additional_info'
    ]


    def __init__(self, db):
        self.db         = db
        self.DBAlarms   = DBAlarms(db)
        self.DBStps     = DBStps(db)
        self.DateHelper = DateHelper()


    def save(self, stpName, alarmsData):

        if alarmsData == False or alarmsData == type(False):
            return False

        stpData = self.DBStps.read({'name': stpName})

        if not stpData or len(stpData) != 1:
            return False

        stpAlarms = self.DBAlarms.read([['stp_id', '=', stpData[0]['id']], ['date_notice_end', 'IS', 'NULL']])

        if stpAlarms == type(False):
            return False

        if isinstance(alarmsData, list) and len(alarmsData) == 0:
            if len(stpAlarms) > 0:
                # Zamykamy wszystkie alarmy, bo nie ma juz zadnego
                for alarm in stpAlarms:
                    self.DBAlarms.update({'date_notice_end': self.DateHelper.getCurrentDateTime()}, {'id': alarm['id']})
            return True

        # Zamykamy stare alarmy, ktore juz nie wystepuja
        for i_stpAlarms in range(len(stpAlarms)):
            stillExists = False
            for i_alarmsData in range(len(alarmsData)):
                if self._compare_alarms(stpAlarms[i_stpAlarms], alarmsData[i_alarmsData]):
                    stillExists = True
                    break
            if not stillExists:
                self.DBAlarms.update({'date_notice_end': self.DateHelper.getCurrentDateTime()}, {'id': stpAlarms[i_stpAlarms]['id']})

        # Dodajemy nowe alarmy
        for i_alarmsData in range(len(alarmsData)):
            newAlarm = True
            for i_stpAlarms in range(len(stpAlarms)):
                if self._compare_alarms(stpAlarms[i_stpAlarms], alarmsData[i_alarmsData]):
                    newAlarm = False
                    break
            if newAlarm:
                alarmsData[i_alarmsData]['stp_id']            = stpData[0]['id']
                alarmsData[i_alarmsData]['date_notice_start'] = self.DateHelper.getCurrentDateTime()
                self.DBAlarms.create(alarmsData[i_alarmsData])

        return True


    def load(self, stpName):

        stpData = self.DBStps.read({'name': stpName})

        if not stpData or len(stpData) != 1:
            return False

        return self.DBAlarms.read({'stp_id': stpData[0]['id']})


    def _compare_alarms(self, alarm1, alarm2):

        for field in self._alarm_cmp_fields:
            if not field in alarm1 or not field in alarm2 or str(alarm1[field]).strip() != str(alarm2[field]).strip():
                return False
        return True
