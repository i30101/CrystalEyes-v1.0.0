"""
Andrew Kim

27 June 2025

Version 1.0.0

Options for CrystalEyes
"""


import json
from pathlib import Path

from src.variables import Variables


class Options:
    """ Options saver and reader """

    def __init__(self):
        # options filepath
        self.OPTIONS_FILEPATH = "../data/options.json"

        # default options {
        self.DEFAULT_OPTIONS = {
            "Theme": "light",
            "DataSavePath": (str(Path.home()) + "\\Documents").replace("\\", "/"),
            "Px": Variables.DEFAULT_PX,
            "Um": Variables.DEFAULT_UM,
            "Scale": Variables.DEFAULT_SCALE,
        }

        # read options
        try:
            with open(self.OPTIONS_FILEPATH) as file:
                self.options = json.load(file)
        except json.JSONDecodeError:
            # if file is empty or corrupted, reset to defaults
            self.options = self.DEFAULT_OPTIONS
        except FileNotFoundError:
            self.options = self.DEFAULT_OPTIONS


    def write_options(self):
        """ Writes options to file """
        with open(self.OPTIONS_FILEPATH, 'w') as file:
            json.dump(self.options, file, indent=4)


    def reset_options(self):
        """ Resets options to default """
        self.options = self.DEFAULT_OPTIONS
        self.write_options()


    def get_theme(self) -> str:
        """ Returns the theme """
        return self.options["Theme"]


    def get_data_save_path(self) -> str:
        """ Returns the data save path """
        return self.options["DataSavePath"]


    def get_px(self) -> float:
        """ Returns the pixel size """
        return self.options["Px"]


    def get_um(self) -> float:
        """ Returns the unit of measurement """
        return self.options["Um"]


    def get_scale(self) -> float:
        """ Returns the unit of measurement """
        return self.options["Scale"]


    def set_theme(self, new_theme: str):
        """ Sets theme for the application """
        self.options["Theme"] = new_theme
        self.write_options()


    def set_data_save_path(self, new_filepath: str):
        """ Sets path for where data is saved """
        self.options["DataSavePath"] = new_filepath


    # TODO add these methods to Gui
    def set_px(self, new_px: float):
        """ Sets pixel count """
        self.options["Px"] = new_px


    def set_um(self, new_um: float):
        """ Sets um count """
        self.options["Um"] = new_um
