import curses
import pyperclip
import logging
from src.gui import MessageBox

class Exporter:


    def __init__(self, screen, window, header, menuHeader):
        self.screen     = screen
        self.window     = window
        self.header     = header
        self.menuHeader = menuHeader
        self.msgBox     = MessageBox.MessageBox(screen, window, header)

        # Tworzymy tablice mapowania z przekazanej wczesniej listy na slownik, aby moc
        # latwo odwolywac sie do kolejnych elementow
        self.headPosList = map(lambda x: x[0], menuHeader)
        self.headPosMapper = {}
        for head in menuHeader:
            self.headPosMapper[head[0]] = head[1]

        return None


    def jira(self, data):

        out = ['||{0}||'.format('||'.join(self.headPosList))]
        for line in data:
            tmpLine = []
            for pos in self.headPosList:
                cell = line[self.headPosMapper[pos]]
                if isinstance(cell, list):
                    cell = ' '.join(map(lambda x: str(x), cell))
                if not isinstance(cell, str):
                    cell = str(cell)
                if cell == '':
                    cell = ' '
                tmpLine.append(cell)
            out.append('|{0}|'.format('|'.join(tmpLine)))

        text = '\n'.join(out)        

        pyperclip.copy(text)
        self.msgBox.showInfo("Data copied to your clipboard", "Jira Export")
