from __future__ import division
import curses
import logging


class Presenter:


    def __init__(self, window, data):
        self.window   = window
        self.allData  = data

        self.spacing  = 5
        self.maxY     = curses.LINES - 10
        self.maxX     = curses.COLS
        self.showFrom = 0

        self.cursorPosition = False
        counter = 0
        for pos in data:
            if 'scroll' in pos and pos['scroll']:
                self.cursorPosition = counter
                break
            counter += 1

        #Nadawanie unikatowych id dla rekordow
        i = 0
        for i in range(len(self.allData)):
            self.allData[i]['_row_id'] = i
            i += 1


    def updateData(self, data):
        self.allData        = data
        self.showFrom       = 0
        self.cursorPosition = False
        logging.fatal(data)
        i = 0
        for i in range(len(self.allData)):
            self.allData[i]['_row_id'] = i
            i += 1


    def refresh(self):

        # Czyszczenie ekranu
        for row in range(1,self.maxY + 2):
            self.window.addstr(row, 1, ' ' * (self.maxX - 2))

        # Wycinamy tylko kawalek z self.allData, ktory zmiesci nam sie na ekranie
        self.dataToShow = self.allData[self.showFrom:self.showFrom + self.maxY]

        rowSize = 0
        for data in self.allData:
            if 'spacer' in data and data['spacer']:
                continue
            if len(data['name']) > rowSize:
                rowSize = len(data['name'])

        row = 1
        dataMenuViewLength = self.spacing + rowSize + 2
        maxDataViewLength  = self.maxX - dataMenuViewLength - 3
        for data in self.dataToShow:
            # Mamy do czynienia z przerywnikiem:
            if 'spacer' in data and data['spacer'] != False:
                self.window.addstr(row, self.spacing + int(rowSize / 2), "{0}".format(data['name']), curses.A_BOLD)
                row += 1
            # Komorka z zawartoscia i prostym tekstem
            elif 'value' in data:
                if data['name'] != '':
                    self.window.addstr(row, self.spacing, "{0}:".format(data['name']), curses.A_BOLD)
                if data['value'] == None:
                    data['value'] = ''
                if self.cursorPosition == self.dataToShow[row - 1]['_row_id']:
                    if 'action' in data and data['action']:
                        self.window.addstr(row, dataMenuViewLength, "{0}".format(str(data['value'])[0:maxDataViewLength]), curses.A_BOLD | curses.A_UNDERLINE)
                    else:
                        self.window.addstr(row, dataMenuViewLength, "{0}".format(str(data['value'])[0:maxDataViewLength]), curses.A_BOLD)
                else:
                    if 'action' in data and data['action']:
                        self.window.addstr(row, dataMenuViewLength, "{0}".format(str(data['value'])[0:maxDataViewLength]), curses.A_UNDERLINE)
                    else:
                        self.window.addstr(row, dataMenuViewLength, "{0}".format(str(data['value'])[0:maxDataViewLength]))
                row += 1


        # Rysujemy slider
        sliderSize = self.maxY
        sliderPos = 0

        if self.allData:
            sliderSize = self.maxY * (self.maxY / len(self.allData))
            if sliderSize < 2:
               sliderSize = 2
            sliderPos = (self.maxY - 1 - sliderSize) * (self.cursorPosition / len(self.allData))

        self.window.addstr(1, self.maxX - 2, '-', curses.A_BOLD)
        drawed = 0
        for y in range(2, self.maxY + 1):
           if y >= (sliderPos + 1) and drawed <= sliderSize:
                self.window.addstr(y, self.maxX - 2, '|', curses.A_BOLD)
                drawed += 1
        self.window.addstr(self.maxY + 1, self.maxX - 2, '-', curses.A_BOLD)

        self.window.refresh()


    def input(self, key):

        viewedIds = map(lambda x: x['_row_id'], self.dataToShow)
        allIds    = map(lambda x: x['_row_id'], self.allData)

        if key == curses.KEY_UP:

            # Nie potrzebujemy niczego przewijac,
            # poprzedni rekord jest w aktualnie wyswietlanych:
            if (self.cursorPosition - 1) in viewedIds:
                self.cursorPosition -= 1
                if not self._isHighlightable(self.cursorPosition):
                    self.input(curses.KEY_UP)
            else:
                if len(viewedIds) == len(allIds):
                    self.cursorPosition = len(viewedIds) - 1
                    if not self._isHighlightable(self.cursorPosition):
                        self.input(curses.KEY_UP)
                else:
                    # Czy poprzedni rekord jest w danych do wyswietlenia
                    if (self.cursorPosition - 1) in allIds:
                        self.cursorPosition -= 1
                        self.showFrom = self.cursorPosition
                        if not self._isHighlightable(self.cursorPosition):
                            self.refresh()
                            self.input(curses.KEY_UP)
                    # Jezeli jestesmy na pierwszym elemencie
                    elif self.cursorPosition == 0:
                        # Przechodzimy do wyswietlania ostatniego rekordu:
                        self.cursorPosition = len(allIds) - 1
                        self.showFrom = len(allIds) - self.maxY
                        if not self._isHighlightable(self.cursorPosition):
                            self.refresh()
                            self.input(curses.KEY_UP)

        elif key == curses.KEY_DOWN:

            # Nie potrzebujemy niczego przewijac,
            # nastepny rekord jest w aktualnie wyswietlanych:
            if (self.cursorPosition + 1) in viewedIds:
                self.cursorPosition += 1
                if not self._isHighlightable(self.cursorPosition):
                    self.input(curses.KEY_DOWN)
            else:
                # Na ekranie wyswietlane sa wszystkie elementy,
                # Przewijamy kursor na pierwszy element:
                if len(viewedIds) == len(allIds):
                    self.cursorPosition = 0
                    if not self._isHighlightable(self.cursorPosition):
                        self.input(curses.KEY_DOWN)
                else:
                    # Czy nastepny rekord jest w danych do wswietlenia
                    if (self.cursorPosition + 1) in allIds:
                        self.cursorPosition += 1
                        self.showFrom       += 1
                        if not self._isHighlightable(self.cursorPosition):
                            self.refresh()
                            self.input(curses.KEY_DOWN)
                    # Jezeli jestesmy na ostatnim elemencie
                    elif self.cursorPosition == len(allIds) - 1:
                        # Przechodzimy do wyswietlania pierwszego rekordu:
                        self.cursorPosition = 0
                        self.showFrom       = self.cursorPosition
                        if not self._isHighlightable(self.cursorPosition):
                            self.refresh()
                            self.input(curses.KEY_DOWN)

        elif key == curses.KEY_NPAGE:
            for x in range(0,10):
                self.input(curses.KEY_DOWN)
        elif key == curses.KEY_PPAGE:
            for x in range(0,10):
                self.input(curses.KEY_UP)

        self.refresh()


    def getAction(self):

        if self.cursorPosition == False or not 'action' in self.allData[self.cursorPosition]:
            return False

        return self.allData[self.cursorPosition]['action']


    def getSelected(self):

        if not self.cursorPosition:
            return False

        return self.allData[self.cursorPosition]['_row_id']


    def _isHighlightable(self, rowId):

        if 'spacer' in self.allData[rowId]:
            return False
        if 'value' in self.allData[rowId] and self.allData[rowId]['value'] == '':
            return False
        return True
