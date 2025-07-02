"""
Andrew Kim

2 July 2025

Version 1.0.0

Data graph for visualizing temperature
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables


class DataGraph:
    """ Data graph for visualizing temperature"""

    def __init__(self, root):
        self.root = root

        # create a bordered box
        self.box = ttk.LabelFrame(self.root, text="Temperature", padding=(10, 10))
        self.box.grid(row=0, column=0, padx=10, pady=Variables.NOPAD_PAD, sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)

        self.frame = ttk.Frame(self.box)
