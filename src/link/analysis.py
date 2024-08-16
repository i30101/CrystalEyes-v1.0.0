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

from src.variables import Variables




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

        # list of areas of contours
        area_px = 0
        area_um = 0

        # ratio sum
        ratios_sum = 0

        for contour in contours:
            # calculate areas
            area_px += len(contour)
            area_um += Analysis.px_to_um(len(contour))

            # find rectangle bounding box and side ratio
            rect = cv2.minAreaRect(contour)
            box = np.intp(cv2.boxPoints(rect))
            sides = [math.dist(box[0], box[1]), math.dist(box[1], box[2])]
            sides.sort()
            ratio = sides[0] / sides[1]
            ratios_sum += ratio

            cv2.drawContours(processed_image, [contour], -1, color=(0, 0, 0, 100), thickness=cv2.FILLED)

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
                ratios_sum / num_contours,
                num_contours
            ]
        )


    @staticmethod
    def get_contours(image: np.ndarray):
        """ Use Cellpose to extract largest contours """
        model = models.Cellpose(gpu=False, model_type='cyto')
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
