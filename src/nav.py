"""
Andrew Kim

27 June 2025

Version 1.0.0

Navigation tabs
"""


import tkinter as tk
from tkinter import ttk
from combo import Combo

from variables import Variables


class Nav1(ttk.Frame):
    """ Navbar tab 1: file options """

    def __init__(self, root):
        super().__init__(root)

        self.open_file_button = ttk.Button(self, text="Open File")
        self.open_file_button.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.clear_button = ttk.Button(self, text="Clear Media")
        self.clear_button.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10)



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



class Nav3(ttk.Frame):
    """ Navbar tab 3: exporting data """

    def __init__(self, root):
        super().__init__(root)

        self.download_label = ttk.Label(self, text="Save to folder:")
        self.download_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.browse_button = ttk.Button(self, text="Browse")
        self.browse_button.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10)

        self.export_path = tk.StringVar()
        self.export_entry = ttk.Entry(self, textvariable=self.export_path, width=38)
        self.export_entry.grid(row=0, column=2, padx=Variables.PAD_NOPAD, pady=10)

        self.processed_images = tk.IntVar()
        self.processed_checkbox = ttk.Checkbutton(
            self,
            variable=self.processed_images,
            text="Save processed",
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



class Nav4(ttk.Frame):
    """ Navbar tab 4: settings """

    def __init__(self, root, theme_change: callable = None):
        super().__init__(root)

        self.on_theme_change = theme_change

        self.theme_label = ttk.Label(self, text="Theme:")
        self.theme_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.theme_combo = Combo(
            self,
            self.on_theme_change,
            values=["Light", "Dark"],
            width=7
        )
        self.theme_combo.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10)

        self.open_fullscreen = tk.IntVar()
        self.fullscreen_checkbox = ttk.Checkbutton(
            self,
            variable=self.open_fullscreen,
            text="Open in fullscreen",
            onvalue=1, offvalue=0
        )
        self.fullscreen_checkbox.grid(row=0, column=2, padx=Variables.PAD_NOPAD)

        self.reset_settings_button = ttk.Button(self, text="Reset Settings")
        self.reset_settings_button.grid(row=0, column=3, padx=Variables.PAD_NOPAD, pady=10)
