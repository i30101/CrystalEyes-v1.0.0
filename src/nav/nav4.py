"""
Andrew Kim

9 July 2025

Version 1.0.0
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables
from src.components.combo import Combo


class Nav4(ttk.Frame):
    """ Navbar tab 4: settings """

    def __init__(self, root, theme_change: callable = None):
        super().__init__(root)

        self.on_theme_change = theme_change

        self.theme_label = ttk.Label(self, text="Theme:")
        self.theme_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.theme_combo = Combo(
            self,
            self.on_theme_change,
            values=["Light", "Dark"],
            width=7
        )
        self.theme_combo.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10)

        self.open_fullscreen = tk.IntVar()
        self.fullscreen_checkbox = ttk.Checkbutton(
            self,
            variable=self.open_fullscreen,
            text="Open in fullscreen",
            onvalue=1, offvalue=0
        )
        self.fullscreen_checkbox.grid(row=0, column=2, padx=Variables.PAD_NOPAD)

        self.reset_settings_button = ttk.Button(self, text="Reset Settings")
        self.reset_settings_button.grid(row=0, column=3, padx=Variables.PAD_NOPAD, pady=10)
