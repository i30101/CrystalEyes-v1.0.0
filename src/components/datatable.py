"""
Andrew Kim

30 June 2025

Version 1.0.0

Data viewing table
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables



class DataTable:
    """ Data previewer """

    def __init__(self, root):
        self.root = root

        # create a bordered box
        self.box = ttk.LabelFrame(self.root, text="Frame Data", padding=(10, 10))
        self.box.grid(row=0, column=0, padx=10, pady=Variables.NOPAD_PAD, sticky="ew")

        # Make the box expand horizontally
        self.root.grid_columnconfigure(0, weight=1)

        # configure grid layout
        self.box.grid_columnconfigure(0, weight=0)
        self.box.grid_columnconfigure(1, weight=0)
        self.box.grid_columnconfigure(2, weight=0)
        self.box.grid_columnconfigure(3, weight=0)

        self.LABEL_WIDTH = 12
        self.ENTRY_WIDTH = 6

        # current frame number
        # TODO make it so that when the frame number changes, other values are updated as well
        # TODO do this in the gui
        self.frame_number = tk.IntVar()
        self.frame_number_label = ttk.Label(self.box, text="Frame number", width=self.LABEL_WIDTH)
        self.frame_number_label.grid(row=0, column=0, padx=0, pady=5, sticky="w")
        self.frame_number_entry = ttk.Entry(self.box, textvariable=self.frame_number, width=self.ENTRY_WIDTH)
        self.frame_number_entry.grid(row=0, column=1, padx=0, pady=5, sticky="ew")

        # # ramp number
        self.ramp = tk.IntVar()
        self.ramp_label = ttk.Label(self.box, text="Ramp number", width=self.LABEL_WIDTH)
        self.ramp_label.grid(row=0, column=2, padx=(30, 0), pady=5, sticky="w")
        self.ramp_entry = ttk.Entry(self.box, textvariable=self.ramp, state="readonly", width=self.ENTRY_WIDTH)
        self.ramp_entry.grid(row=0, column=3, padx=0, pady=5, sticky="ew")

        # temperature
        self.temperature = tk.DoubleVar()
        self.temperature_label = ttk.Label(self.box, text="Temperature", width=self.LABEL_WIDTH)
        self.temperature_label.grid(row=1, column=0, padx=0, pady=5, sticky="w")
        self.temperature_entry = ttk.Entry(self.box, textvariable=self.temperature, state="readonly", width=self.ENTRY_WIDTH)
        self.temperature_entry.grid(row=1, column=1, padx=0, pady=5, sticky="ew")

        # temperature limit
        self.limit = tk.DoubleVar()
        self.limit_label = ttk.Label(self.box, text="Limit", width=self.LABEL_WIDTH)
        self.limit_label.grid(row=1, column=2, padx=(30, 0), pady=5, sticky="w")
        self.limit_entry = ttk.Entry(self.box, textvariable=self.limit, state="readonly", width=self.ENTRY_WIDTH)
        self.limit_entry.grid(row=1, column=3, padx=0, pady=5, sticky="ew")

        # temperature rate
        self.rate = tk.DoubleVar()
        self.rate_label = ttk.Label(self.box, text="Rate", width=self.LABEL_WIDTH)
        self.rate_label.grid(row=2, column=0, padx=0, pady=5, sticky="w")
        self.rate_entry = ttk.Entry(self.box, textvariable=self.limit, state="readonly", width=self.ENTRY_WIDTH)
        self.rate_entry.grid(row=2, column=1, padx=0, pady=5, sticky="ew")


    def set_data(self, frame_number: int, ramp: int, temperature: float, limit: float, rate: float):
        """ Sets the data in the entry boxes """
        self.frame_number.set(frame_number)
        self.ramp.set(ramp)
        self.temperature.set(temperature)
        self.limit.set(limit)
        self.rate.set(rate)

        # set all entries to readonly
        self.frame_number_entry.config(state="readonly")
        self.ramp_entry.config(state="readonly")
        self.temperature_entry.config(state="readonly")
        self.limit_entry.config(state="readonly")
        self.rate_entry.config(state="readonly")


    def clear_data(self):
        """ Clears the data in the entry boxes """
        self.frame_number.set(0)
        self.ramp.set(0)
        self.temperature.set(0.0)
        self.limit.set(0.0)
        self.rate.set(0.0)

        # set all entries to readonly
        self.frame_number_entry.config(state="readonly")
        self.ramp_entry.config(state="readonly")
        self.temperature_entry.config(state="readonly")
        self.limit_entry.config(state="readonly")
        self.rate_entry.config(state="readonly")