"""
Andrew Kim

1 July 2025

Version 1.0.0
"""


import numpy as np
import pandas as pd


class LinkamDataFile:
    """ Linkam Data File object """

    def __init__(self,
                 file: str,
                 d: str,
                 ramp: list[int],
                 temp: list[float],
                 temp_limit: list[float],
                 temp_rate: list[float],
                 raw: list[np.ndarray]):
        """ Linkam Data File object """
        self.filepath = file
        self.date = d
        self.ramps = ramp
        self.temperatures = temp
        self.temperature_limits = temp_limit
        self.temperature_rates = temp_rate

        # calculate beforehand
        # TODO might want to remove if not needed
        self.length = len(ramp)
        self.frame_numbers = list(range(self.length))

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


    def dataset_summary(self) -> str:
        """ Creates summary for analyzed dataset """
        # TODO make summary
        return str(self.length)


    def to_df(self) -> pd.DataFrame:
        """ Converts data to DataFrame """
        # TODO make DataFrame
        # TODO figure out a good way to format
        self.data = 0
        return pd.DataFrame(None)