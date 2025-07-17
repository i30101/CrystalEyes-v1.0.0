"""
Andrew Kim

30 June 2025

Version 1.0.0

Data viewing table
"""


import tkinter as tk
from tkinter import ttk

from databox import DataBox

class DataTable(DataBox):
    """ Data previewer """

    def __init__(self, root):
        super().__init__(root, "Frame Data")

        # configure grid layout
        self.box.grid_columnconfigure(0, weight=0)
        self.box.grid_columnconfigure(1, weight=0)
        self.box.grid_columnconfigure(2, weight=0)
        self.box.grid_columnconfigure(3, weight=0)

        self.LABEL_WIDTH = 12
        self.ENTRY_WIDTH = 6

        # current frame number
        self.frame_number = tk.IntVar()
        self.frame_number_label = ttk.Label(self.box, text="Frame number", width=self.LABEL_WIDTH)
        self.frame_number_label.grid(row=0, column=0, padx=0, pady=5, sticky="w")
        self.frame_number_entry = ttk.Entry(self.box, textvariable=self.frame_number, width=self.ENTRY_WIDTH)
        self.frame_number_entry.grid(row=0, column=1, padx=0, pady=5, sticky="ew")

        # number of frames
        self.frames = tk.IntVar()
        self.frames_label = ttk.Label(self.box, text="Frames", width=self.LABEL_WIDTH)
        self.frames_label.grid(row=0, column=2, padx=(30, 0), pady=5, sticky="w")
        self.frames_entry = ttk.Entry(self.box, textvariable=self.frames, state="readonly", width=self.ENTRY_WIDTH)
        self.frames_entry.grid(row=0, column=3, padx=0, pady=5, sticky="ew")

        # temperature
        self.temperature = tk.DoubleVar()
        self.temperature_label = ttk.Label(self.box, text="Temp (°C)", width=self.LABEL_WIDTH)
        self.temperature_label.grid(row=1, column=0, padx=0, pady=5, sticky="w")
        self.temperature_entry = ttk.Entry(self.box, textvariable=self.temperature, state="readonly", width=self.ENTRY_WIDTH)
        self.temperature_entry.grid(row=1, column=1, padx=0, pady=5, sticky="ew")

        # temperature limit
        self.limit = tk.DoubleVar()
        self.limit_label = ttk.Label(self.box, text="Limit (°C)", width=self.LABEL_WIDTH)
        self.limit_label.grid(row=1, column=2, padx=(30, 0), pady=5, sticky="w")
        self.limit_entry = ttk.Entry(self.box, textvariable=self.limit, state="readonly", width=self.ENTRY_WIDTH)
        self.limit_entry.grid(row=1, column=3, padx=0, pady=5, sticky="ew")

        # temperature rate
        self.rate = tk.DoubleVar()
        self.rate_label = ttk.Label(self.box, text="Rate (°C/min)", width=self.LABEL_WIDTH)
        self.rate_label.grid(row=2, column=0, padx=0, pady=5, sticky="w")
        self.rate_entry = ttk.Entry(self.box, textvariable=self.rate, state="readonly", width=self.ENTRY_WIDTH)
        self.rate_entry.grid(row=2, column=1, padx=0, pady=5, sticky="ew")

        # ramp number
        self.ramp = tk.IntVar()
        self.ramp_label = ttk.Label(self.box, text="Ramp", width=self.LABEL_WIDTH)
        self.ramp_label.grid(row=2, column=2, padx=(30, 0), pady=5, sticky="w")
        self.ramp_entry = ttk.Entry(self.box, textvariable=self.ramp, state="readonly", width=self.ENTRY_WIDTH)
        self.ramp_entry.grid(row=2, column=3, padx=0, pady=5, sticky="ew")



    def set_data(self,
                 frame_number: int,
                 frames: int,
                 temperature: float,
                 limit: float,
                 rate: float,
                 ramp: int ):
        """ Sets the data in the entry boxes """
        # Only update frame_number if entry does not have focus
        if self.frame_number_entry.focus_get() != self.frame_number_entry:
            self.frame_number.set(frame_number)
        self.frames.set(frames)
        self.temperature.set(temperature)
        self.limit.set(limit)
        self.rate.set(rate)
        self.ramp.set(ramp)

        # set all entries to readonly
        self.frames_entry.config(state="readonly")
        self.temperature_entry.config(state="readonly")
        self.limit_entry.config(state="readonly")
        self.rate_entry.config(state="readonly")
        self.ramp_entry.config(state="readonly")


    def clear_data(self):
        """ Clears the data in the entry boxes """
        self.set_data(0, 0, 0.0, 0.0, 0.0, 0)
