"""
Andrew Kim

17 June 2025

Version 0.9.0

Splash screen
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

from variables import Variables


class Splash:
    def __init__(self, root):
        """ Splash screen to run before main GUI """
        self.root = root
        self.SPLASH_WIDTH = 600
        self.SPLASH_HEIGHT = 400
        self.ROUND_RADIUS = 7
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.x_coord = (self.screen_width / 2) - (self.SPLASH_WIDTH / 2)
        self.y_coord = (self.screen_height / 2) - (self.SPLASH_HEIGHT / 2)

        self.root.geometry("%dx%d+%d+%d" % (self.SPLASH_WIDTH, self.SPLASH_HEIGHT, self.x_coord, self.y_coord))
        self.root.overrideredirect(1)

        # Set transparent background color
        self.root.config(bg='black')
        self.root.wm_attributes('-transparentcolor', 'black')

        # Create a rounded-corner mask for the splash image
        mask = Image.new('L', (self.SPLASH_WIDTH, self.SPLASH_HEIGHT), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            [(0, 0), (self.SPLASH_WIDTH, self.SPLASH_HEIGHT)],
            radius=self.ROUND_RADIUS,
            fill=255
        )

        self.raw = Image.open(Variables.SPLASH_PATH).convert("RGBA")
        self.image = self.raw.resize((self.SPLASH_WIDTH, self.SPLASH_HEIGHT), Image.Resampling.LANCZOS)
        self.image.putalpha(mask)

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background_label = tk.Label(self.root, image=self.background_image, borderwidth=0, highlightthickness=0, bg='black')
        self.background_label.place(x=0, y=0, width=self.SPLASH_WIDTH, height=self.SPLASH_HEIGHT)

        self.root.after(3000, self.root.destroy)
        self.root.mainloop()
