"""
Andrew Kim

1 July 2025

Version 1.0.0

Media manager
"""


import numpy as np

from src.media.empty import EmptyContainer
from src.media.mediaviewer import MediaViewer


class Viewer:
    """ Media manager for GUI """

    def __init__(self, root, no_media_func: callable):
        self.root = root

        self.uploaded = False

        self.empty_container = EmptyContainer(self.root, no_media_func)
        self.media_viewer = MediaViewer(self.root)


    def show_media(self, images: list[np.ndarray]):
        """ Show media viewer """
        self.uploaded = True
        self.empty_container.hide()
        self.media_viewer.hide()
        self.media_viewer.show_media(images)


    def clear_media(self):
        """ Clear media viewer """
        self.uploaded = False
        self.media_viewer.hide()
        self.empty_container.show()
