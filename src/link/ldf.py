"""
Andrew Kim

1 July 2025

Version 1.0.0
"""


from datetime import datetime

import numpy as np
import pandas as pd

from src.link.analysis import Analysis


class LinkamDataFile:
    """ Linkam Data File object """

    def __init__(self,
                 file: str,
                 ramp: list[int],
                 temp: list[float],
                 temp_limit: list[float],
                 temp_rate: list[float],
                 raw: list[np.ndarray]):
        """ Linkam Data File object """
        self.filepath = file
        # self.date = d
        self.ramps = ramp
        self.temperatures = temp
        self.temperature_limits = temp_limit
        self.temperature_rates = temp_rate

        self.raw_images = raw

        # to be set after processing
        self.processed_images = None
        self.data = None


    def get_data(self, frame_number: int) -> tuple:
        """ Returns data in tuple form for given frame number """
        return (
            frame_number,
            self.ramps[frame_number],
            self.temperatures[frame_number],
            self.temperature_limits[frame_number],
            self.temperature_rates[frame_number]
        )


    def trim(self, start: int, end: int) -> 'LinkamDataFile':
        """ Trims the data file to a specific range of frames """

        trimmed_file = LinkamDataFile(
            file=self.filepath,
            ramp=self.ramps[start:end],
            temp=self.temperatures[start:end],
            temp_limit=self.temperature_limits[start:end],
            temp_rate=self.temperature_rates[start:end],
            raw=self.raw_images[start:end]
        )

        return trimmed_file


    def analyze(self) -> None:
        """ Analyzes raw images and extracts data """

        self.processed_images = []
        self.data = [[] for _ in range(7)]

        for image in self.raw_images:
            analyzed_image, analyzed_data = Analysis.analyze_image(image)
            print("image analyzed")
            # append processed image
            self.processed_images.append(analyzed_image)

            for i, variable in enumerate(analyzed_data):
                self.data[i].append(variable)


    def to_df(self) -> pd.DataFrame:
        """ Converts analyzed data to DataFrame (one row per frame) """
        columns = {
            "Frame number": list(range(1, len(self.raw_images) + 1)),
            "Temperature (°C)": self.temperatures,
            "Temperature limit (°C)": self.temperature_limits,
            "Temperature rate (°C/min)": self.temperature_rates,
            "Ramp number": self.ramps,
            "Average area (px²)": self.data[0],
            "Average area (µm²)": self.data[1],
            "Total area (px²)": self.data[2],
            "Total area (µm²)": self.data[3],
            "Density (crystals/µm²)": self.data[4],
            "Coverage (%)": self.data[5],
            "Number of contours": self.data[6]
        }
        return pd.DataFrame(columns)


    def data_summary(self) -> str:
        """ Creates summary of extracted data """
        output = f"\nAnalyzed Linkam Data File: {self.filepath}"
        output += f"\n    Number of frames: {len(self.raw_images)}"
        output += f"\n    Ending temperature: {self.temperatures[-1]} °C"
        output += f"\n    Temperature ramp: {self.ramps[0]} °C/min"
        return output
