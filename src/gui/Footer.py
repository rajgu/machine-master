import curses
from src.db import DBAlarms
from src.db import DBStps
from src.db import DBJobs
from src.db import DBJobsSuites
from src.db import DBUsers

class Footer:

    def __init__(self, db):
        self.db           = db
        self.DBAlarms     = DBAlarms.DBAlarms(db)
        self.DBStps       = DBStps.DBStps(db)
        self.DBJobs       = DBJobs.DBJobs(db)
        self.DBJobsSuites = DBJobsSuites.DBJobsSuites(db)
        self.DBUsers      = DBUsers.DBUsers(db)
        self.window       = curses.newwin(3, curses.COLS, curses.LINES - 3, 0)
        self.window.border(0)
        self.window.refresh()

    def refresh(self):
        stps_count   = self.DBStps.read({}, {'count': True})
        jobs_count   = self.DBJobs.read({}, {'count': True})
        ups_count    = self.DBJobs.read([['up', '!=', '""']], {'fields': 'up', 'count': True, 'distinct': True})
        tss_count    = self.DBJobsSuites.read([['suite', '!=', '""']], {'fields': 'suite', 'count': True, 'distinct': True})
        users_count  = self.DBUsers.read([['signum', '!=', '""']], {'count': True})
        alarms_count = self.DBAlarms.read([['date_notice_end', 'IS', 'NULL']], {'count': True})

        text = "In db: {0} STPs, {1} JOBs, {2} UPs, {3} Users, {4} TSs, {5} Alarms".format(stps_count, jobs_count, ups_count, users_count, tss_count, alarms_count)

        self.window.addstr(1, int((curses.COLS - len(text)) / 2), text)
        self.window.refresh()
