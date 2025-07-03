"""
Andrew Kim

3 July 2025

Version 1.0.0

Ramp selector
"""


import tkinter as tk
from tkinter import ttk

from src.data.databox import DataBox

from src.components.combo import Combo


class RampBox(DataBox):
    """ Ramp selector """

    def __init__(self, root, on_ramp_select: callable = None):
        super().__init__(root, "Ramp Analysis")

        self.on_ramp_select = on_ramp_select

        # Ramp selection dropdown
        self.ramp_combo = Combo(
            self.box,
            self.on_ramp_change,
            values=[""],
            width=7
        )

        self.change_num_options(4)

        self.ramp_combo.grid(row=0, column=0, padx=(10, 15), pady=5, sticky="ew")

        self.ramp_temperature = tk.DoubleVar()
        self.temperature_label = ttk.Label(self.box, text="Ramp limit", width=8)
        self.temperature_label.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="w")
        self.temperature_entry = ttk.Entry(self.box, textvariable=self.ramp_temperature, state="readonly", width=4)
        self.temperature_entry.grid(row=0, column=2, padx=(10, 0), pady=5, sticky="ew")

        self.analyze_button = ttk.Button(self.box, text="Analyze", command=self.on_ramp_change)
        self.analyze_button.grid(row=0, column=3, padx=(20, 0), pady=5, sticky="ew")



    def change_num_options(self, new_num: int):
        new_values = [f"Ramp {i+1}" for i in range(new_num)]

        self.ramp_combo['values'] = new_values

        self.ramp_combo.set(new_values[0])

    def on_ramp_change(self):
        return