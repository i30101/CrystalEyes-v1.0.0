"""
Andrew Kim

3 July 2025

Version 1.0.0

Template box for data display
"""


import tkinter as tk
from tkinter import ttk

from variables import Variables


class DataBox:
    """ Template box for data display """

    def __init__(self, root, title: str):
        self.root = root

        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.X, expand=False)

        self.box = ttk.LabelFrame(self.container, text=title, padding=(10, 10))
        self.box.grid(row=0, column=0, padx=10, pady=Variables.NOPAD_PAD, sticky="ew")

        self.container.grid_columnconfigure(0, weight=1)
