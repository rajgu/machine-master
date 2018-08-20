import curses
from src.gui import List
from src.gui import AlarmsWindow
from src.gui import StpsWindow
from src.gui import JobsWindow
from src.gui import UPsWindow
from src.gui import UsersWindow
from src.gui import MessageBox
from src.gui import TestSuitesWindow
from src.helpers import KeysHelper
import logging

class MainWindow:


    menuHeader = [
        ['Name'       , 'name'],
        ['Description', 'desc']
    ]

    menuData = [
        {'name': 'STPs',        'desc': 'List of all STPs'},
        {'name': 'Jobs',        'desc': 'List of newest 10000 jobs'},
        {'name': 'UPs',         'desc': 'List of all UPs'},
        {'name': 'Users',       'desc': 'List of all Users'},
        {'name': 'Test Suites', 'desc': 'List of all Test Suites'},
        {'name': 'Alarms',      'desc': 'List of all Active Alarms'},
    ]


    def __init__(self, db, screen, header, finder, footer):
        self.db = db
        self.screen = screen
        self.header = header
        self.finder = finder
        self.footer = footer
        self.window = curses.newwin(curses.LINES - 7, curses.COLS, 4, 0)
        self.window.border(0)
        self.window.refresh()


    def enter(self):
        selected = self.list.getSelected()

        if selected == 0:
            window = StpsWindow.StpsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer)
        if selected == 1:
            window = JobsWindow.JobsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer)
        if selected == 2:
            window = UPsWindow.UPsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer)
        if selected == 3:
            window = UsersWindow.UsersWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer)
        if selected == 4:
            window = TestSuitesWindow.TestSuitesWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer)
        if selected == 5:
            window = AlarmsWindow.AlarmsWindow(self.db, self.screen, self.window, self.header, self.finder, self.footer)

        window.init()
        self.list.refresh()
        self.window.refresh()


    def init(self):

        self.header.addPosition('Menu')
        self.list = List.List(self.window, self.finder, self.menuData, self.menuHeader)
        self.list.refresh()

        keysHelper = KeysHelper.KeysHelper()
        while 1:
            key = self.screen.getch()

            if key not in keysHelper.getAll():
                continue

            if key in keysHelper.getEscape():
                msgBox = MessageBox.MessageBox(self.screen, self.window, self.header)
                answer = msgBox.askTrueFalse("Are you sure you want to quit?", "Quit?")
                self.list.refresh()
                if answer:
                    break

            if key in keysHelper.getNavigation():
                self.list.input(key)

            if key in keysHelper.getEnter():
                self.enter()

