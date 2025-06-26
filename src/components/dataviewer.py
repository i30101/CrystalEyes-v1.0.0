"""
Andrew Kim

30 June 2025

Version 1.0.0

Data viewing table
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables



class DataViewer:
    """ Data previewer """

    def __init__(self, root):
        self.root = root

        # Configure grid columns to allow entry column to expand
        self.root.grid_columnconfigure(0, weight=0)  # label column
        self.root.grid_columnconfigure(1, weight=1)  # entry column

        self.LABEL_WIDTH = 20
        self.ENTRY_WIDTH = 20

        # current frame number
        self.frame_number = tk.IntVar()
        self.frame_number_label = ttk.Label(self.root, text="Frame number:", width=self.LABEL_WIDTH)
        self.frame_number_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10, sticky="w")
        self.frame_number_entry = ttk.Entry(self.root, textvariable=self.frame_number, state="readonly", width=self.ENTRY_WIDTH)
        self.frame_number_entry.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10, sticky="ew")

        # temperature
        self.temperature = tk.DoubleVar()
        self.temperature_label = ttk.Label(self.root, text="Temperature:", width=self.LABEL_WIDTH)
        self.temperature_label.grid(row=1, column=0, padx=Variables.PAD_NOPAD, pady=10, sticky="w")
        self.temperature_entry = ttk.Entry(self.root, textvariable=self.temperature, state="readonly", width=self.ENTRY_WIDTH)
        self.temperature_entry.grid(row=1, column=1, padx=Variables.PAD_NOPAD, pady=10, sticky="ew")

        # TODO maybe add temperature symbol at the end