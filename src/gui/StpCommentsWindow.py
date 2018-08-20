import curses
import logging
from src.gui import List
from src.helpers import Exporter
from src.helpers import KeysHelper


class StpCommentsWindow:


    menuHeader = [
        ['Date'  , 'date'],
        ['Text'  , 'text'],
        ['Ticket', 'ticket']
    ]


    def __init__(self, db, screen, window, header, finder, footer, comments):
        self.db       = db
        self.screen   = screen
        self.header   = header
        self.finder   = finder
        self.footer   = footer
        self.comments = comments
        self.window   = window
        self.window.border(0)
        self.window.refresh()


    def init(self):

        self.oldFilter = self.finder.getData()
        self.finder.clear()

        self.header.addPosition('Comments')

        self.list = List.List(self.window, self.finder, self.comments, self.menuHeader)
        self.list.refresh()

        keysHelper = KeysHelper.KeysHelper()
        exporter   = Exporter.Exporter(self.screen, self.window, self.header, self.menuHeader)

        while 1:
            key = self.screen.getch()

            if key not in keysHelper.getAll():
                continue

            if key in keysHelper.getEscape():
                self.finder.clear()
                break

            if key in keysHelper.getExport():
                exporter.jira(self.list.getFilteredData())
                self.list.refresh()

            if key in keysHelper.getNavigation():
                self.list.input(key)

            if key in keysHelper.getInput():
                self.finder.input(key)
                self.list.refresh()

        self.header.removePosition()
        self.finder.clear()
