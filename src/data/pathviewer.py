"""
Andrew Kim

1 July 2025

Version 1.0.0

Filepath viewing box
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables

from src.data.databox import DataBox


class PathViewer(DataBox):
    """ Filepath viewing box """

    def __init__(self, root):
        super().__init__(root, "Opened file")

        # configure grid layout
        self.box.grid_columnconfigure(0, weight=1)

        # filepath label
        self.filepath = tk.StringVar()
        self.filepath_entry = ttk.Entry(self.box, textvariable=self.filepath, state="readonly", width=100)
        self.filepath_entry.grid(row=0, column=0, padx=0, pady=5, sticky="ew")



    def set_filepath(self, filepath: str):
        """ Sets the filepath in the entry box """
        self.filepath.set(filepath)
        self.filepath_entry.config(state="readonly")


    def clear_filepath(self):
        """ Clears the filepath in the entry box """
        self.filepath.set("")
        self.filepath_entry.config(state="readonly")