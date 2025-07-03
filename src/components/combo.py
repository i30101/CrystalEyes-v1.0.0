"""
Andrew Kim

3 July 2025

Version 1.0.0

Combo box widget
"""


from tkinter import ttk


class Combo(ttk.Combobox):
    """ Simplified Combobox container """

    def __init__(self,
                 root,
                 update: callable,
                 values: list[str],
                 **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self['values'] = values
        self.current(0)
        self.state(["readonly"])
        self.bind("<<ComboboxSelected>>", self.modified)
        self.on_update = update


    def modified(self, _):
        """ Calls stored method after Combo option is changed """
        self.on_update()
