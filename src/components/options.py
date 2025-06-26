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
        # options filepath (relative to project root)
        self.OPTIONS_FILEPATH = str(Path(__file__).parent.parent.parent / "data" / "options.json")

        # default options {
        self.DEFAULT_OPTIONS = {
            "Theme": "light",
            "ExportPath": (str(Path.home()) + "\\Documents").replace("\\", "/"),
            "Px": Variables.DEFAULT_PX,
            "Um": Variables.DEFAULT_UM,
            "Scale": Variables.DEFAULT_SCALE,
            "SaveProcessed": 1,
            "SaveRaw": 1
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
        Path(self.OPTIONS_FILEPATH).parent.mkdir(parents=True, exist_ok=True)
        with open(self.OPTIONS_FILEPATH, 'w') as file:
            json.dump(self.options, file, indent=4)


    def reset_options(self):
        """ Resets options to default """
        self.options = self.DEFAULT_OPTIONS
        self.write_options()


    def get_theme(self) -> str:
        """ Returns the theme """
        return self.options["Theme"]


    def get_export_path(self) -> str:
        """ Returns the data save path """
        return self.options["ExportPath"]


    def get_px(self) -> float:
        """ Returns the pixel size """
        return self.options["Px"]


    def get_um(self) -> float:
        """ Returns the unit of measurement """
        return self.options["Um"]


    def get_scale(self) -> float:
        """ Returns the unit of measurement """
        return self.options["Scale"]


    def get_processed_checkbox(self) -> int:
        """ Returns preference for exporting processed images """
        return self.options["SaveProcessed"]


    def get_raw_checkbox(self) -> int:
        """ Returns preference for exporting raw images """
        return self.options["SaveRaw"]


    def set_theme(self, new_theme: str):
        """ Sets theme for the application """
        self.options["Theme"] = new_theme
        self.write_options()


    def set_export_path(self, new_filepath: str):
        """ Sets path for where data is saved """
        self.options["ExportPath"] = new_filepath


    def set_scale(self, new_scale: float):
        """ Sets scale """
        self.options["Scale"] = new_scale


    def set_px(self, new_px: float):
        """ Sets pixel count """
        self.options["Px"] = new_px


    def set_um(self, new_um: float):
        """ Sets um count """
        self.options["Um"] = new_um


    def set_processed_checkbox(self, new_processed: bool):
        """ Sets preference for saving processed images """
        self.options["SaveProcessed"] = new_processed


    def set_raw_checkbox(self, new_raw: bool):
        """ Sets preference for saving raw images """
        self.options["SaveRaw"] = new_raw