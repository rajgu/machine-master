import curses

class KeysHelper:

    enter = [curses.KEY_ENTER, 343, 10]

    escape = [27]

    navigation = [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_NPAGE, curses.KEY_PPAGE]

    inputed = range(32, 126) + [curses.KEY_BACKSPACE]

    export = [266]


    def __init__(self):
        self.allKeys = self.enter + self.escape + self.navigation + self.inputed + self.export


    def getAll(self):
        return self.allKeys


    def getEnter(self):
        return self.enter


    def getEscape(self):
        return self.escape


    def getNavigation(self):
        return self.navigation


    def getInput(self):
        return self.inputed


    def getExport(self):
        return self.export
