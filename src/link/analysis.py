"""
Andrew Kim

7 July 2025

Version 1.0.0

Analysis module for CrystalEyes
"""

import cv2
import numpy as np
# TODO find a way to not use pytesseract
from datetime import datetime

from cellpose import models, io
from src.variables import Variables


# TODO update variables


class Analysis:
    """ Image analyzer """

    model = models.CellposeModel()

    scale = Variables.DEFAULT_SCALE

    # ################################ GENERAL METHODS ################################ #

    @staticmethod
    def average(data: list, r: int = -1) -> float:
        """ Finds average of dataset """
        avg = sum(data) / len(data)
        return round(avg, r) if r > -1 else avg

    @staticmethod
    def total(data: list, r: int = -1) -> float:
        """ Finds total of dataset """
        tot = sum(data)
        return round(tot, r) if r > -1 else tot

    @staticmethod
    def crop(image, xs: list, ys: list) -> np.ndarray:
        """ Crops image to custom size """
        return image[ys[0]: ys[1], xs[0]: xs[1]]

    @staticmethod
    def polygon_area(contour) -> float:
        """ Finds area of contour polygon """
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        return cv2.contourArea(approx)

    @staticmethod
    def to_time(time: str) -> datetime:
        """ Converts string into datetime object """
        return datetime.strptime(time, "%H:%M:%S")

    @staticmethod
    def px_to_um(area_px: float, r: int = -1) -> float:
        """ Converts an area in square pixels to square micrometers """
        area = area_px * (Analysis.scale ** 2)
        return round(area, r) if r > -1 else area

    @staticmethod
    def set_scale(new_scale: float):
        """ Sets new scale in um per px """
        Analysis.scale = new_scale

    # ################################ ANALYSIS METHODS ################################ #

    @staticmethod
    def analyze_image(image: np.ndarray) -> tuple[np.ndarray, list]:
        """ Analyze image and return AnalyzedImage object """

        # processed image that will display contours
        processed_image = image.copy()

        # calculate area of image
        image_area_um = Analysis.px_to_um(len(image)) * Analysis.px_to_um(len(image[0]))

        contours = Analysis.get_contours(image)

        # list of areas of contours
        area_px = 0
        area_um = 0

        for contour in contours:
            # calculate areas
            area_px += len(contour)
            area_um += Analysis.px_to_um(area_px)

            # draw filled contour with random transparent color
            random_color = (np.random.randint(0, 255, size=3) + [100]).tolist()
            cv2.drawContours(processed_image, [contour], -1, color=random_color, thickness=cv2.FILLED)

        # number of contours
        num_contours = len(contours)

        return (
            processed_image,
            [
                round(area_px / num_contours, 3),
                round(area_um / num_contours, 3),
                round(area_px, 3),
                round(area_um, 3),
                round(num_contours / image_area_um, 3),
                round(area_um / image_area_um, 3),
                num_contours
            ]
        )





    @staticmethod
    def get_contours(image: np.ndarray):
        """ Use Cellpose to extract largest contours """
        print("Getting contours using Cellpose")
        masks, _, _, _ = Analysis.model.eval(image, diameter=50, channels=[0, 0])
        rois = list(masks)
        contour_points = [[] for _ in masks]
        for y, roi in enumerate(rois):
            for x, contour_num in enumerate(roi):
                contour_points[contour_num].append([x, y])

        # return contours that are sufficiently large
        return [
            np.array(point_list, dtype=np.int32).reshape(-1, 1, 2)
            for point_list in contour_points[1:] if len(point_list) > 500
        ]
