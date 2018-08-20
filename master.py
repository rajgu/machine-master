#!/usr/bin/env python
from __future__ import division
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/modules/')

import curses
import logging
import traceback
from src import Config
from src import DBConnection
from src.gui import Footer
from src.gui import Finder
from src.gui import Header
from src.gui import MainWindow
from math import *


screen = curses.initscr()

curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
screen.border(0)
curses.curs_set(0)


config = Config.Config()
db = DBConnection.DBConnection(config).connect()

screen.refresh()

footer = Footer.Footer(db)
footer.refresh()

finder = Finder.Finder()
finder.refresh()

header = Header.Header()
header.refresh()

main = MainWindow.MainWindow(db, screen, header, finder, footer)

try:
    main.init()
except Exception as e:
    logging.fatal("Exception: {0}".format(e))
finally:
    curses.endwin()
    if traceback.format_exc().strip() != "None":
        print traceback.format_exc()
