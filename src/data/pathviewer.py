"""
Andrew Kim

1 July 2025

Version 1.0.0

Filepath viewing box
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables


class PathViewer:
    """ Filepath viewing box """

    def __init__(self, root):
        self.root = root

        # create a bordered box
        self.box = ttk.LabelFrame(self.root, text="Opened file", padding=(10, 10))
        self.box.grid(row=0, column=0, padx=10, pady=Variables.NOPAD_PAD, sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)

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