"""
Andrew Kim

27 June 2025

Version 1.0.0

Global variables and constants
"""


class Variables:
    """ Global variables and constants """

    """ App Name """
    APP_NAME = "CrystalEyes v1.0.0"

    """ File paths """
    ICON_PATH = "assets/icon.png"
    SPLASH_PATH = "assets/splash.png"


    """ GUI padding"""
    PAD_NOPAD = (10, 0)
    NOPAD_PAD = (0, 10)


    """ Cropping defaults """
    MAX_Y = 1536
    MAX_X = 2048


    """ Default pixel scale """
    DEFAULT_PX = 808.669


    """ Default micrometer scale """
    DEFAULT_UM = 100


    """ Default scale """
    DEFAULT_SCALE = round(DEFAULT_UM / DEFAULT_PX, 5)


    """ Default font """
    # TODO maybe this needs updating?


    """ Width of left panel """
    LEFT_WIDTH = 0.7


    """ Width of right panel """
    RIGHT_WIDTH = 0.3


    """ Image and video formats """
    IMAGE_TYPES = [".jpg", ".png", ".jpeg", ".tiff", ".bmp"]
    VIDEO_TYPES = [".mp4", ".avi", ".mov", ".mkv"]


    """ Options for images and video media"""
    IMAGE_OPTIONS = ["Area in px²", "Area in µm²", "Side ratios", "# of sides"]
    VIDEO_OPTIONS = ["# of objects", "Average area", "Total area", "Temperature", "# of sides"]


    # TODO do these have to be fixed?
    # TODO merge with options.py?

    """ Filepath for image media export """
    image_filepath = None


    """ Filepath for video media export """
    video_filepath = None
