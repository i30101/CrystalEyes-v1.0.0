"""
Andrew Kim

3 July 2025

Version 1.0.0

Ramp selector
"""


import tkinter as tk
from tkinter import ttk

from src.data.databox import DataBox


class RampBox(DataBox):
    """ Ramp selector """

    def __init__(self, root, on_ramp_select: callable = None):
        super().__init__(root, "Ramp Selector")

        self.on_ramp_select = on_ramp_select

        # Ramp selection dropdown
        self.ramp_var = tk.StringVar()
        self.ramp_dropdown = ttk.Combobox(self.box, textvariable=self.ramp_var, state="readonly")
        self.ramp_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.ramp_dropdown.bind("<<ComboboxSelected>>", self.on_ramp_change)


    def on_ramp_change(self):
        return