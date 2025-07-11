"""
Andrew Kim

1 July 2025

Version 1.0.0
"""


import time
import numpy as np
import pandas as pd

from src.link.analysis import Analysis


def slope(x1: float, x2: float, delta: int) -> float:
    return (x2 - x1) / delta


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
        self.ramps = ramp
        self.temperatures = temp
        self.temperature_limits = temp_limit
        self.temperature_rates = temp_rate

        self.raw_images = raw

        # to be set after processing
        self.processed_images = None
        self.data = None
        self.image_areas = None


    def get_data(self, frame_number: int) -> tuple:
        """ Returns data in tuple form for given frame number """
        return (
            frame_number,
            len(self.raw_images),
            self.temperatures[frame_number],
            self.temperature_limits[frame_number],
            self.temperature_rates[frame_number],
            self.ramps[frame_number]
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
        self.data = [[] for _ in range(8)]
        self.image_areas = []

        analyzed_times = []

        for i, image in enumerate(self.raw_images):
            t0 = time.time()
            analyzed_image, analyzed_data = Analysis.analyze_image(image)
            t1 = time.time()
            print(f"Image analyzed in {t1 - t0:.3f} seconds")
            analyzed_times.append(round(t1 - t0, 3))

            # append processed image
            self.processed_images.append(analyzed_image)

            for variable in enumerate(analyzed_data):
                if i == len(analyzed_data) - 1:
                    continue

                self.data[i].append(variable)

            for area in analyzed_data[8]:
                self.image_areas.append({
                    "frame": i + 1,
                    "area_px": area,
                })



        # find rate of area change over time
        average_area_um = self.data[1]
        average_area_rate = []
        for i, area in enumerate(average_area_um):
            if i == 0:
                average_area_rate.append(slope(area, average_area_um[i + 1], 1))
            elif i == len(average_area_um) - 1:
                average_area_rate.append(slope(average_area_um[i - 1], area, 1))
            else:
                average_area_rate.append(slope(average_area_um[i - 1], average_area_um[i + 1], 2))
        self.data.append(average_area_rate)

        self.data.append(analyzed_times)


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
            "Rate of area change (µm²/min)": self.data[8],
            "Total area (px²)": self.data[2],
            "Total area (µm²)": self.data[3],
            "Density (crystals/µm²)": self.data[4],
            "Coverage (%)": self.data[5],
            "Side ratio": self.data[6],
            "Number of contours": self.data[7],
            "Duration of analysis (s)": self.data[9]
        }
        return pd.DataFrame(columns)


    def area_to_df(self) -> pd.DataFrame:
        """ Converts image areas to Dataframe (one row per area) """
        return pd.DataFrame(self.image_areas)


    def data_summary(self) -> str:
        """ Creates summary of extracted data """
        output = f"Analyzed Linkam Data File: {self.filepath}"
        output += f"\n    Number of frames: {len(self.raw_images)}"
        output += f"\n    Ending temperature: {self.temperatures[-1]} °C"
        output += f"\n    Temperature ramp: {self.ramps[0]} °C/min"
        return output
