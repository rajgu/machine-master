import curses
import logging
from src.helpers import KeysHelper


class MessageBox:


    def __init__(self, screen, window, header):
        self.screen = screen
        self.window = window
        self.header = header
        self.height, self.width = window.getmaxyx()


    def askTrueFalse(self, text, header=False):

        if header:
            self.header.addPosition(header)

        textLen = len(text)
        minWidth = 14 if textLen + 4 < 14 else textLen + 4
        minHeight = 5

        self.yesPosition = int(round(minWidth / 3 * 1, 0))
        self.noPosition  = int(round(minWidth / 3 * 2, 0))

        windowPositionX = int(round((self.width - minWidth) / 2))
        windowPositionY = int(round((self.height - minHeight) / 2))

        self.boxWindow = curses.newwin(minHeight, minWidth, windowPositionY, windowPositionX)
        self.boxWindow.border(0)

        self.boxWindow.addstr(1, 2, text)

        self.selected = False
        self.boxWindow.addstr(3, self.yesPosition, 'Yes')
        self.boxWindow.addstr(3, self.noPosition, 'No', curses.A_BOLD)

        self.boxWindow.refresh()
        self._trueFalseLoop()

        if header:
            self.header.removePosition()

        return self.selected


    def showInfo(self, text, header=False):

        if header:
            self.header.addPosition(header)

        textLen = len(text)
        minWidth = 14 if textLen + 4 < 14 else textLen + 4
        minHeight = 5

        self.okPosition = int(round(minWidth / 2 -1, 0))

        windowPositionX = int(round((self.width - minWidth) / 2))
        windowPositionY = int(round((self.height - minHeight) / 2))

        self.boxWindow = curses.newwin(minHeight, minWidth, windowPositionY, windowPositionX)

        self.boxWindow.border(0)
        self.boxWindow.addstr(1, 2, text)
        self.boxWindow.addstr(3, self.okPosition, 'OK', curses.A_BOLD)

        self.boxWindow.refresh()
        self._enterLoop()

        if header:
            self.header.removePosition()

        return True


    def _trueFalseLoop(self):

        keysHelper = KeysHelper.KeysHelper()
        while 1:
            key = self.screen.getch()

            if key in keysHelper.getEscape():
                self.selected = False
                break

            if key in keysHelper.getNavigation():
                self.selected = True if self.selected == False else False
                if self.selected == True:
                    self.boxWindow.addstr(3, self.yesPosition, 'Yes', curses.A_BOLD)
                    self.boxWindow.addstr(3, self.noPosition, 'No')
                else:
                    self.boxWindow.addstr(3, self.yesPosition, 'Yes')
                    self.boxWindow.addstr(3, self.noPosition, 'No', curses.A_BOLD)

                self.boxWindow.refresh()

            if key in keysHelper.getEnter():
                break


    def _enterLoop(self):

        keysHelper = KeysHelper.KeysHelper()
        while 1:
            key = self.screen.getch()

            if key in keysHelper.getEscape() + keysHelper.getEnter():
                return True
