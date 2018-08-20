import curses
import logging
from src.db import DBJobsSuites
from src.gui import List
from src.gui import SuiteWindow
from src.helpers import Exporter
from src.helpers import KeysHelper


class TestSuitesWindow:


    menuHeader = [
        ['Name'  , 'suite'],
        ['Executions' , 'count']
    ]


    def __init__(self, db, screen, window, header, finder, footer):
        self.db           = db
        self.DBJobsSuites = DBJobsSuites.DBJobsSuites(db)
        self.screen       = screen
        self.header       = header
        self.finder       = finder
        self.footer       = footer
        self.window       = window
        self.window.border(0)
        self.window.refresh()


    def enter(self):
        selected = self.list.getSelected()
        self.oldFilter = self.finder.getData()
        self.finder.clear()

        window = SuiteWindow.SuiteWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer, self.suitesList[selected]['suite'])
        window.init()

        self.finder.setData(self.oldFilter)
        self.list.refresh()
        self.window.refresh()


    def init(self):

        self.header.addPosition('Test Suites List')
        self.suitesList = self.DBJobsSuites.read([['suite', '!=', '""']], {'fields': ['suite', 'COUNT(suite) AS count'], 'groupBy': 'suite', 'sort': 'ASC', 'order': 'suite'})

        self.list = List.List(self.window, self.finder, self.suitesList, self.menuHeader)
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
