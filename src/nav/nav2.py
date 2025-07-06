"""
Andrew Kim

30 June 2025

Version 1.0.0

Navigation tab 2
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables


class Nav2(ttk.Frame):
    """ Navbar tab 2: image scaling options """

    def __init__(self, root):
        super().__init__(root)

        self.scale_label = ttk.Label(self, text="Scale:")
        self.scale_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

        self.scale_input = tk.StringVar()
        self.scale_entry = ttk.Entry(self, textvariable=self.scale_input, width=10)
        self.scale_entry.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

        self.unit_label = ttk.Label(self, text="μm / px")
        self.unit_label.grid(row=0, column=2, padx=(5, 15), pady=Variables.PAD_NOPAD)

        self.px_input = tk.StringVar()
        self.px_entry = ttk.Entry(self, textvariable=self.px_input, width=10)
        self.px_entry.grid(row=0, column=3, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

        self.px_label = ttk.Label(self, text="pixels is equal to ")
        self.px_label.grid(row=0, column=4, padx=(5, 0), pady=Variables.PAD_NOPAD)

        self.um_input = tk.StringVar()
        self.um_entry = ttk.Entry(self, textvariable=self.um_input, width=10)
        self.um_entry.grid(row=0, column=5, padx=(5, 0), pady=Variables.PAD_NOPAD)

        self.um_label = ttk.Label(self, text="μm")
        self.um_label.grid(row=0, column = 6, padx=(5, 15), pady=Variables.PAD_NOPAD)

        self.reset_scale_button = ttk.Button(self, text="Reset")
        self.reset_scale_button.grid(row=0, column=7, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)
