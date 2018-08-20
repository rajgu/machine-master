import curses
import logging

class Finder:
    def __init__(self):
        self.window = curses.newwin(1, curses.COLS, 3, 0)
        self.searchTextHeader = 'Filter: '
        self.searchText = ''


    def input(self, keyCode):
        if keyCode == curses.KEY_BACKSPACE:
            self.searchText = self.searchText[0: len(self.searchText) - 1]
        else:
            key = chr(keyCode)
            if (len(self.searchText) + len(self.searchTextHeader)) < (curses.COLS - 3):
                self.searchText = "{0}{1}".format(self.searchText, key)

        self.refresh()


    def refresh(self):
        self.window.addstr(0, 0, ' ' * (curses.COLS - 1))
        if self.searchText:
            self.window.addstr(0, 2, self.searchTextHeader)
            self.window.addstr(0, 2 + len(self.searchTextHeader), self.searchText)
        self.window.refresh()


    def getData(self):
        return self.searchText


    def setData(self, data):
        self.searchText = data
        self.refresh()


    def clear(self):
        self.searchText = ''
        self.refresh()

