import curses
import logging


class Header:


	def __init__(self):
		self.window    = curses.newwin(3, curses.COLS, 0, 0)
		self.positions = []
		self.maxX      = curses.COLS - 4
		self.window.border(0)
		self.window.refresh()


	def addPosition(self, position):
		self.positions.append(position)
		self.refresh()


	def removePosition(self):
		if len(self.positions) > 0:
			del self.positions[-1]
		self.refresh()


	def input(self, key):
		self.refresh()


	def refresh(self):
		self.window.addstr(1, 1, ' ' * int(self.maxX + 1))

		if len(self.positions) == 0:
			return

		text = ' -> '.join(self.positions)

		if len(text) > self.maxX:
			text = text[len(text) - self.maxX:]
		text = text.split(' -> ')

		self.window.addstr(1, 2, text[0])
		length = len(text[0])
		if len(text) > 1:
			for i in range(1, len(text)):
				self.window.addstr(1, 2 + length, ' -> ', curses.A_BOLD)
				length += 4
				self.window.addstr(1, 2 + length, text[i])
				length += len(text[i])

		self.window.refresh()
