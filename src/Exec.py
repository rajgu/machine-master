#!/usr/bin/env python2

import webbrowser


class Exec:


    def __init__(self, data):
        self.data = data
        return None


    def init(self):
        if self.data[0:4] == 'http':
            webbrowser.get('firefox').open_new_tab(self.data)
        if self.data[0:1] == '/':
            webbrowser.get('firefox').open_new_tab(self.data)