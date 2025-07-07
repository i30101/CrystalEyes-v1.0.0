"""
Andrew Kim

30 June 2025

Version 1.0.0

Navigation tab 3
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables


class Nav3(ttk.Frame):
    """ Navbar tab 3: exporting data """

    def __init__(self, root):
        super().__init__(root)

        self.download_label = ttk.Label(self, text="Save to folder:")
        self.download_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.browse_button = ttk.Button(self, text="Browse")
        self.browse_button.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10)

        self.export_path = tk.StringVar()
        self.export_entry = ttk.Entry(self, textvariable=self.export_path, width=30)
        self.export_entry.grid(row=0, column=2, padx=Variables.PAD_NOPAD, pady=10)

        self.processed_images = tk.IntVar()
        self.processed_checkbox = ttk.Checkbutton(
            self,
            variable=self.processed_images,
            text="Save processed images",
            onvalue=1, offvalue=0
        )
        self.processed_checkbox.grid(row=0, column=3, padx=Variables.PAD_NOPAD, pady=10)

        self.raw_images = tk.IntVar()
        self.raw_checkbox = ttk.Checkbutton(
            self,
            variable=self.raw_images,
            text="Save raw",
            onvalue=1, offvalue=0
        )
        self.raw_checkbox.grid(row=0, column=4, padx=10, pady=10)

        self.download_button = ttk.Button(self, text="Save Data")
        self.download_button.grid(row=0, column=5, padx=Variables.PAD_NOPAD, pady=10)
