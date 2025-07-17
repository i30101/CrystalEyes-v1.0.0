"""
Andrew Kim

7 July 2025

Version 1.0.0

Analysis module for CrystalEyes
"""


import math
import cv2
import numpy as np
from cellpose import models

from variables import Variables




class Analysis:
    """ Image analyzer """

    scale = Variables.DEFAULT_SCALE

    # ################################ GENERAL METHODS ################################ #

    @staticmethod
    def px_to_um(area_px: float) -> float:
        """ Converts an area in square pixels to square micrometers """
        area = area_px * (Analysis.scale ** 2)
        return area

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
        image_area_um = Analysis.px_to_um(len(image) * len(image[0]))

        contours = Analysis.get_contours(image)

        # area list in px²
        areas_px = []

        # ratio sum
        ratios_sum = 0

        for contour in contours:
            # calculate areas
            areas_px.append(len(contour))

            # find rectangle bounding box and side ratio
            rect = cv2.minAreaRect(contour)
            box = np.intp(cv2.boxPoints(rect))
            sides = [math.dist(box[0], box[1]), math.dist(box[1], box[2])]
            sides.sort()
            ratio = sides[0] / sides[1]
            ratios_sum += ratio

            # draw contour
            cv2.drawContours(processed_image, [contour], -1, color=(0, 0, 0, 100), thickness=cv2.FILLED)

        # number of contours
        num_contours = len(contours)

        # area list in µm²
        areas_um = list(map(
            lambda x: round(Analysis.px_to_um(x), 3),
            areas_px
        ))

        # total areas
        area_px = sum(areas_px)
        area_um = sum(areas_um)

        return (
            processed_image,
            [
                round(area_px / num_contours, 3), # average area in px²
                round(area_um / num_contours, 3), # average area in µm²
                round(area_px, 3), # total area in px²
                round(area_um, 3), # total area in µm²
                round(num_contours / image_area_um, 3), # density in crystals/µm²
                round(area_um / image_area_um, 3), # coverage ratio
                round(ratios_sum / num_contours, 5), # side ratio
                num_contours, # number of contours
                areas_um # list of areas in µm²
            ]
        )


    @staticmethod
    def get_contours(image: np.ndarray):
        """ Use Cellpose to extract largest contours """
        model = models.Cellpose()
        masks, _, _, _ = model.eval(image, diameter=50, channels=[0, 0])
        rois = list(masks)
        contour_points = [[] for _ in masks]
        for y, roi in enumerate(rois):
            for x, contour_num in enumerate(roi):
                contour_points[contour_num].append([x, y])

        contours = []
        for point_list in contour_points[1 :]:
            if len(point_list) > 500:
                contours.append(np.array(point_list, dtype=np.int32).reshape((-1, 1, 2)))

        return contours
