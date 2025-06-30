"""
Andrew Kim

27 June 2025

Version 1.0.0

Graphical user interface for CrystalEyes app
"""

import tkinter as tk
from tkinter import ttk, filedialog
# import sv_ttk

from ctypes import windll

from src.components.console import Console
from src.nav.nav1 import Nav1
from src.variables import Variables

# components
from src.components.options import Options

# containers



windll.shcore.SetProcessDpiAwareness(1)



class Gui:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.title(Variables.APP_NAME)

        self.options = Options()


        # ################################ LEFT COLUMN ################################ #

        self.left_column = ttk.Frame(self.root)
        self.left_column.place(relwidth=Variables.LEFT_WIDTH, relheight=1)
        self.left = ttk.Frame(self.left_column)
        self.left.pack(fill=tk.BOTH, expand=True, padx=(20, 10), pady=20)


        # ################ TABS ################ #
        self.tab_control = ttk.Notebook(self.left)

        self.tab1 = Nav1(self.tab_control)

        self.tab_control.add(self.tab1, text="File")

        self.tab_control.pack(fill=tk.X, pady=Variables.NOPAD_PAD, expand=False)


        # ################ PANED WINDOW ################ #
        self.paned_window = ttk.PanedWindow(self.left, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # media panel
        self.media_frame = ttk.Frame(self.paned_window, height=1, padding=(0, 10))
        self.paned_window.add(self.media_frame, weight=10)
        # TODO add viewer

        # console
        self.console_frame = ttk.Frame(self.paned_window, height=1)
        self.paned_window.add(self.console_frame, weight=1)
        self.console = Console(self.console_frame)


        # ################################ RIGHT COLUMN ################################ #
        self.right_column = ttk.Frame(self.root)
        self.right_column.place(relx=Variables.LEFT_WIDTH, relwidth=Variables.RIGHT_WIDTH, relheight=1)
        self.right = ttk.Frame(self.right_column)
        self.right.pack(fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)


        # ################ DATA VIEWER ################ #
        self.data_viewer = ttk.Frame(self.right_column)
        self.data_viewer.place(relwidth=Variables.RIGHT_WIDTH, relheight=0.5)
        # TODO add data viewer


        # TODO potentially add controls in between


        # ################ DATA GRAPH ################ #
        self.data_graph = ttk.Frame(self.right_column)
        self.data_graph.place(rely=0.5, relwidth=Variables.RIGHT_WIDTH, relheight=0.5)
        # TODO add data graph



        # TODO set theme
        self.root.after(100, lambda: self.root.state('zoomed'))
        # TODO add self.onclose
        # self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        # run GUI
        self.root.mainloop()