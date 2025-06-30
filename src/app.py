"""
Andrew Kim

27 June 2025

Version 1.0.0

CrystalEyes: A Python application for analyzing images of nano-ice crystals.
This app automates the extraction of ice crystal features, such as size and frequency
from images of a sample taken over a period of time.

This app supports Linkam Data Files in the .ldf format.
Individual frames or a series of frames can be analyzed by the app.

The machine learning algorithm is powered by Cellpose, a software designed to identify cytoplasm from cells.
Using a graphics card is highly recommended to accelerate the Cellpose algorithm.
"""



import tkinter as tk

from gui import Gui
from src.components.splash import Splash



def main():
    """ Starts the app by running the splash screen """

    root = tk.Tk()

    # set app icon for the splash window
    # icon = tk.PhotoImage(file='assets/icon.png', master=root)
    # root.iconphoto(False, icon)

    splash = Splash(root)

    start()


def start():
    window = tk.Tk()

    # set up app icon for main window
#     icon = tk.PhotoImage(file='assets/icon.png', master=window)
#     window.iconphoto(False, icon)

    gui = Gui(window)


if __name__ == '__main__':
    main()
