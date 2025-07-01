"""
Andrew Kim

1 July 2025

Version 1.0.0

Viewer for series of images in LDF file
"""


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import re

from src.containers.container import MediaContainer


class MediaViewer(MediaContainer):
    """ Container for showing series of images in LDF file """

    def __init__(self, root):
        super().__init__(root)

        # TODO change pause and play buttons
        self.PAUSE = "⏸"
        self.PLAY = "▶"
        self.DELAY = 100
        self.BUTTON_PADDING = 4
        self.DEFAULT_DURATION = 60

        self.playing_now = False

        # TODO see if this can be switched to ttk
        self.video_label = tk.Label(self.container)


