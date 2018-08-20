from __future__ import division
import curses
import logging


class List:


    def __init__(self, window, finder, data, header):
        self.window         = window
        self.finder         = finder
        self.allData        = data
        self.dataToShow     = []
        self.header         = header
        self.spacing        = 3

        self.maxY           = curses.LINES - 10
        self.maxX           = curses.COLS

        self.showFrom       = 0
        self.showDirection  = 'DOWN'
        self.oldFilter      = 0

        self.numPositions   = len(data)
        self.cursorPosition = 0
        self.sortBy         = False
        self.refreshFilter  = False

        # Tworzymy tablice mapowania z przekazanej wczesniej listy na slownik, aby moc
        # latwo odwolywac sie do kolejnych elementow
        self.headPosList = map(lambda x: x[0], self.header)
        self.headPosMapper = {}
        for head in self.header:
            self.headPosMapper[head[0]] = head[1]

        # liczymy ile wersow zajmie dany rekord i przypisujemy im numery identyfikacyjne:
        for i in range(len(self.allData)):
            self.allData[i]['_row_size'] = self._calculateRowSize(self.allData[i])
            self.allData[i]['_row_id'] = i


    def _takeElement(self, elem):

        if isinstance(elem[self.sortByField], list):
            if len(elem[self.sortByField]) == 0:
                return None

            allEmpty  = True
            allDigits = True
            summ      = 0

            for element in elem[self.sortByField]:
                if element == '':
                    continue
                if isinstance(element, int) or element.isdigit():
                    summ += int(element)
                else:
                    allDigits = False
                    break
                allEmpty = False

            if allDigits:
                return summ
            return elem[self.sortByField][0]

        if isinstance(elem[self.sortByField], str) and elem[self.sortByField].isdigit():
            return int(elem[self.sortByField])

        return elem[self.sortByField]


    def sortData(self):
        self.sortByField = self.headPosMapper[self.sortBy]

        self.allData = sorted(self.allData, key=self._takeElement, reverse=True)
        self.refreshFilter = True


    def refresh(self):

        # Filtrujemy dane do wyswietlenie na liscie
        filterString    = self.finder.getData().lower()
        self.dataToShow = []

        if filterString and ':' in filterString:
            filterSliced = filterString.lower().split(':')
            filterField  = filterSliced[0]
            filterString = filterSliced[1]
        else:
            filterField = False

        if filterString and (self.refreshFilter or self.oldFilter != filterString):
            self.showFrom       = 0
            self.refreshFilter  = False
            self.cursorPosition = 0
            self.oldFilter      = filterString
            self.listData       = []
            self.showDirection  = 'DOWN'

            for listPos in self.allData:
                for headPos in self.headPosList:
                    if ((not filterField) or (filterField and headPos.lower().find(filterField) != -1)) and filterString in str(listPos[self.headPosMapper[headPos]]).lower():
                        self.listData.append(listPos)
                        break
        elif not filterString:
            self.oldFilter = ''
            self.listData  = self.allData

        # Nadajemy lokalne id-ki do rekordow:
        self.filteredDataSize = len(self.listData)
        if self.filteredDataSize > 0:
            #  and '_local_row_id' not in self.listData[0]
            for i in range(self.filteredDataSize):
                self.listData[i]['_local_row_id'] = i

        # Liczymy ile maksymalnie znakow potrzebujemy do numerowania rekordow
        countChars = len(str(len(self.allData)))

        # Ustalamy poczatkowy rozmiar dla dlugosci pola, naglowka, oraz jego poczatkowej zawartosci (czyli naglowka)
        # Python przepisuje obiekty przez referencje, dlatego robimy to w ten sposob
        maxLen     = {}
        headersLen = {}
        for headPos in self.headPosList:
            maxLen[headPos]     = len(headPos)
            headersLen[headPos] = len(headPos)

        # Sprawdzamy, czy jestesmy w stanie wyswietlic pelne naglowki w liscie
        # Jezeli nie - konczymy prace
        if (sum(maxLen.values()) + (len(maxLen) * self.spacing) + countChars + 2) > (self.maxX - (self.spacing * 2)):
            self.window.addstr(1, 1, "Can't write list, resolution too low")
            self.window.refresh()
            return

        # Liczymy maksymalna dlugosc dla danego pola
        # Mozemy tutaj rowniez przekazac liste z wieloma rekordami
        for listPos in self.listData:
            for headPos in self.headPosList:
                if isinstance(listPos[self.headPosMapper[headPos]], list):
                    for item in listPos[self.headPosMapper[headPos]]:
                        if len(str(item)) > maxLen[headPos]:
                            maxLen[headPos] = len(str(item))
                elif len(str(listPos[self.headPosMapper[headPos]])) > maxLen[headPos]:
                    maxLen[headPos] = len(str(listPos[self.headPosMapper[headPos]]))

        # Sprawdzamy, czy wszystkie dane zmieszcza sie w rozdzielczosci wybranej przez uzytkownika i jezeli nie -
        # Zmniejszamy najdluzsze pole, do czasu, az sie nie zmiesci
        while (sum(maxLen.values()) + (len(maxLen) * self.spacing) + countChars + 2) > (self.maxX - (self.spacing * 2)):
            longestField = False
            for key, length in maxLen.iteritems():
                if (length > headersLen[key] and not longestField) or (longestField and length > headersLen[key] and length > maxLen[longestField]):
                    longestField = key
            if longestField:
                maxLen[longestField] -= 1

        # Czyscimy poprzednia zawartosc ekranu
        for row in range(1, self.maxY + 2):
            self.window.addstr(row, 1, ' ' * (self.maxX - 2))

        # Drukujemy naglowek listy, w zaleznosci od tego czy mamy ustawione sortowanie
        offset = countChars + 3
        for listPos in self.header:
            if self.sortBy == listPos[0]:
                self.window.addstr(1, offset, listPos[0], curses.color_pair(2))
            else:
                self.window.addstr(1, offset, listPos[0], curses.A_BOLD)

            offset += maxLen[listPos[0]] + self.spacing


        rowIndex              = self.showFrom
        recordsShowSize       = 0
        # Wyswietlamy wszystkie elementy mieszczace sie na ekranie zaczynajac od tego wskazanego przez showFrom, idac w DOL
        if self.showDirection == 'DOWN':
            while True:
                if rowIndex < self.filteredDataSize and \
                    recordsShowSize + self.listData[rowIndex]['_row_size'] <= self.maxY:
                    self.dataToShow.append(self.listData[rowIndex])
                    recordsShowSize += self.listData[rowIndex]['_row_size']
                    rowIndex += 1
                else:
                    break
        else:
            while True:
                if rowIndex >= 0 and \
                    recordsShowSize + self.listData[rowIndex]['_row_size'] <= self.maxY:
                    self.dataToShow.append(self.listData[rowIndex])
                    recordsShowSize += self.listData[rowIndex]['_row_size']
                    rowIndex -= 1
                else:
                    break

        # Przycinamy rekordy do okreslonej dlugosci
        for i in range(len(self.dataToShow)):
            for view, mapper in self.headPosMapper.iteritems():
                if isinstance(self.dataToShow[i][mapper], list):
                    subItemAdd = []
                    for elem in self.dataToShow[i][mapper]:
                        subItemAdd.append(str(elem)[0:maxLen[view]])
                    self.dataToShow[i][mapper] = subItemAdd
                else:
                    self.dataToShow[i][mapper] = str(self.dataToShow[i][mapper])[0:maxLen[view]]

        # Wyswietlamy rekordy na ekranie, biorac pod uwage kierunek wyswietlania
        # Dla kierunku z gory na dol odwracamy liste i wyliczamy odpowiednio wiersz pierwszego rekordu
        if self.showDirection == 'DOWN':
            row = 2
        else:
            reversed(self.dataToShow)
            row = self.maxY - self.dataToShow[0]['_row_size'] + 2

        # Drukujemy same dane
        for i in range(len(self.dataToShow)):
            rowLocalId = str(self.dataToShow[i]['_local_row_id'] + 1)
            self.window.addstr(row, 1, "{0}{1}".format(' ' * (countChars - len(str(rowLocalId)) + 1), str(rowLocalId)), curses.A_BOLD)
            offset = countChars + 3

            # Dla kazdego naglowka
            for headerPos in self.header:
                # Jezeli rekord jest wybrany:
                if self.cursorPosition == self.dataToShow[i]['_local_row_id']:
                    # Jezeli jest lista, to wypisujemy po kolej kazdy element, bez zmiany offsetu
                    if isinstance(self.dataToShow[i][headerPos[1]], list):
                        tmpRow = row
                        for item in self.dataToShow[i][headerPos[1]]:
                            self.window.addstr(tmpRow, offset, str(item), curses.A_BOLD)
                            tmpRow += 1
                    else:
                        self.window.addstr(row, offset, str(self.dataToShow[i][headerPos[1]]), curses.A_BOLD)
                else:
                    # Operujemy na liscie, na elemencie nie zaznaczonym
                    if isinstance(self.dataToShow[i][headerPos[1]], list):
                        tmpRow = row
                        for item in self.dataToShow[i][headerPos[1]]:
                            if filterField:
                                if filterField in headerPos[1].lower():
                                    self._printFilteredString(tmpRow, offset, item, filterString)
                                else:
                                    self._printFilteredString(tmpRow, offset, item, '')
                            else:
                                self._printFilteredString(tmpRow, offset, item, filterString)
                            tmpRow += 1
                    # Operujemy na zwyklym stringu
                    else:
                        if filterField:
                            if filterField in headerPos[1].lower():
                                self._printFilteredString(row, offset, self.dataToShow[i][headerPos[1]], filterString)
                            else:
                                self._printFilteredString(row, offset, self.dataToShow[i][headerPos[1]], '')
                        else:
                            self._printFilteredString(row, offset, self.dataToShow[i][headerPos[1]], filterString)
                offset += maxLen[headerPos[0]] + self.spacing

            # Odpowiednio ustawiamy kolejny wiersz, w zaleznosci od tego w ktorym kierunku drukujemy:
            if self.showDirection == 'DOWN':
                row += self.dataToShow[i]['_row_size']
            else:
                # zmniejszamy rozmiar wiersza o wielkosc poprzedniego rekordu,
                # jezeli takowy istnieje
                if i + 1 < len(self.dataToShow):
                    row -= self.dataToShow[i + 1]['_row_size']


        # Rysujemy slider
        sliderSize = self.maxY
        sliderPos = 0

        if self.listData:
            sliderSize = self.maxY * (self.maxY / len(self.listData))
            if sliderSize < 2:
               sliderSize = 2
            sliderPos = (self.maxY - 1 - sliderSize) * (self.cursorPosition / len(self.listData))

        self.window.addstr(1, self.maxX - 2, '-', curses.A_BOLD)
        drawed = 0
        for y in range(2, self.maxY + 1):
           if y >= (sliderPos + 1) and drawed <= sliderSize:
                self.window.addstr(y, self.maxX - 2, '|', curses.A_BOLD)
                drawed += 1
        self.window.addstr(self.maxY + 1, self.maxX - 2, '-', curses.A_BOLD)

        self.window.refresh()


    def getFilteredData(self):
        return self.listData


    def input(self, key):

        if not self.dataToShow:
            return

        viewedIds = map(lambda x: x['_local_row_id'], self.dataToShow)
        allIds    = map(lambda x: x['_local_row_id'], self.listData)

        if key == curses.KEY_UP:

            # Nie potrzebujemy niczego przewijac,
            # poprzedni rekord jest w aktualnie wyswietlanych:
            if (self.cursorPosition - 1) in viewedIds:
                self.cursorPosition -= 1
            else:
                if len(viewedIds) == len(allIds):
                    self.cursorPosition = len(viewedIds) - 1
                else:
                    # Czy poprzedni rekord jest w danych do wyswietlenia
                    # zmieniamy kierunek wyswietlania
                    if (self.cursorPosition - 1) in allIds:
                        self.cursorPosition -= 1
                        self.showDirection = 'DOWN'
                        self.showFrom = self.cursorPosition
                    # Jezeli jestesmy na pierwszym elemencie
                    elif self.cursorPosition == 0:
                        # Przechodzimy do wyswietlania ostatniego rekordu:
                        self.cursorPosition = len(allIds) - 1
                        self.showFrom = self.cursorPosition
                        self.showDirection = 'UP'

        elif key == curses.KEY_DOWN:

            # Nie potrzebujemy niczego przewijac,
            # nastepny rekord jest w aktualnie wyswietlanych:
            if (self.cursorPosition + 1) in viewedIds:
                self.cursorPosition += 1
            else:
                # Na ekranie wyswietlane sa wszystkie elementy,
                # Przewijamy kursor na pierwszy element:
                if len(viewedIds) == len(allIds):
                    self.cursorPosition = 0
                else:
                    # Czy nastepny rekord jest w danych do wyswietlenia
                    # zmieniamy kierunek wyswietlania
                    if (self.cursorPosition + 1) in allIds:
                        self.cursorPosition += 1
                        self.showDirection = 'UP'
                        self.showFrom = self.cursorPosition
                    # Jezeli jestesmy na ostatnim elemencie
                    elif self.cursorPosition == len(allIds) - 1:
                        # Przechodzimy do wyswietlania pierwszego rekordu:
                        self.cursorPosition = 0
                        self.showFrom       = self.cursorPosition
                        self.showDirection  = 'DOWN'

        elif key == curses.KEY_NPAGE:
            for x in range(0,10):
                self.input(curses.KEY_DOWN)

        elif key == curses.KEY_PPAGE:
            for x in range(0,10):
                self.input(curses.KEY_UP)

        elif key == curses.KEY_LEFT:
            if self.sortBy == False:
                self.sortBy = self.headPosList[-1]
            else:
                sortFieldId = self.headPosList.index(self.sortBy)
                if sortFieldId == 0:
                    self.sortBy = self.headPosList[-1]
                else:
                    self.sortBy = self.headPosList[sortFieldId - 1]
            self.showFrom       = 0
            self.cursorPosition = 0
            self.showDirection  = 'DOWN'
            self.sortData()

        elif key == curses.KEY_RIGHT:
            if self.sortBy == False:
                self.sortBy = self.headPosList[0]
            else:
                sortFieldId = self.headPosList.index(self.sortBy)
                if sortFieldId == len(self.headPosList) - 1:
                    self.sortBy = self.headPosList[0]
                else:
                    self.sortBy = self.headPosList[sortFieldId + 1]
            self.sortData()
            self.showFrom       = 0
            self.cursorPosition = 0
            self.showDirection  = 'DOWN'

        self.refresh()


    # Zwraca id aktualnie pokazywanego rekordu
    def getSelected(self):

        if self.listData and len(self.listData) > 0:
            return self.listData[self.cursorPosition]['_row_id']
        return False

    # Wylicza, ile linii wyswietlanych zajmuje dany rekord
    def _calculateRowSize(self, row):
        size = 1
        for key, value in row.iteritems():
            if isinstance(value, list):
                if len(value) > size:
                    size = len(value)
        return size


    # Drukuje wskazany ciag znakow w wyznaczonym miejscu i jednoczesnie koloruje wedle zadanego filtru
    def _printFilteredString(self, row, offset, string, filterString):
        lowered = str(string).lower()
        filterSize = len(filterString)
        if filterString and filterString in lowered:
            lastOffset = 0
            findOffset = lowered.find(filterString, 0)
            while findOffset != -1:

                self.window.addstr(row, offset + lastOffset, string[lastOffset:findOffset])
                self.window.addstr(row, offset + findOffset, string[findOffset:findOffset + filterSize], curses.A_BOLD)

                findOffset += filterSize
                lastOffset = findOffset
                findOffset = lowered.find(filterString, findOffset)

                if findOffset == -1:
                    self.window.addstr(row, offset + lastOffset, string[lastOffset:len(string)])

        else:
            self.window.addstr(row, offset, str(string))

