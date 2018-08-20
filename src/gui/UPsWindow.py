import curses
import logging
from src.db import DBJobs
from src.gui import UPWindow
from src.gui import StpWindow
from src.gui import List
from src.helpers import Exporter
from src.helpers import KeysHelper


class UPsWindow:


    menuHeader = [
        ['Name',       'name'],
        ['Product',    'product'],
        ['Revision',   'revision'],
        ['Jobs Count', 'count'],
        ['Upgrade?',   'upgrade']
    ]


    def __init__(self, db, screen, window, header, finder, footer):
        self.db     = db
        self.DBJobs = DBJobs.DBJobs(self.db)
        self.screen = screen
        self.header = header
        self.finder = finder
        self.footer = footer
        self.window = window
        self.window.border(0)
        self.window.refresh()


    def enter(self):
        selected = self.list.getSelected()
        self.oldFilter = self.finder.getData()
        self.finder.clear()

        if selected == type(False):
            return

        window = UPWindow.UPWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.upsList[selected])

        window.init()

        self.finder.setData(self.oldFilter)
        self.list.refresh()
        self.window.refresh()


    def init(self):

        self.header.addPosition('UPs List')
        upsList = self.DBJobs.read({}, {'fields': ['up', 'COUNT(id) AS count'], 'groupBy': 'up', 'order': 'up', 'sort': 'DESC'})

        self.upsList = []
        for up in upsList:
            if not up['up']:
                continue

            parts = up['up'].split('-')
            self.upsList.append({
                'name'    : up['up'],
                'product' : parts[0],
                'revision': parts[1] if len(parts) > 1 else '',
                'count'   : up['count'],
                'upgrade' : 1 if len(up['up'].split('R')) > 2 else 0
            })


        self.list = List.List(self.window, self.finder, self.upsList, self.menuHeader)
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
