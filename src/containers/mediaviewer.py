"""
Andrew Kim

1 July 2025

Version 1.0.0

Viewer for series of images in LDF file
"""


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import numpy as np

from src.containers.container import MediaContainer


class MediaViewer(MediaContainer):
    """ Container for showing series of images in LDF file """

    def __init__(self, root):
        super().__init__(root)

        self.media = None
        self.duration = 0

        # TODO change pause and play buttons
        self.PAUSE = "⏸"
        self.PLAY = "▶"
        self.DELAY = 100
        self.BUTTON_PADDING = 4
        self.DEFAULT_DURATION = 60

        self.playing_now = False

        # TODO see if this can be switched to ttk
        self.video_label = tk.Label(self.container)

        # video timeline container
        self.video_timeline_container = ttk.Frame(self.container)
        self.video_timeline_container.pack(fill=tk.X, side=tk.BOTTOM)

        self.current_frame = tk.IntVar(self.video_timeline_container)
        self.video_timeline = ttk.Scale(self.video_timeline_container,
                                        variable=self.current_frame,
                                        to=self.DEFAULT_DURATION,
                                        orient=tk.HORIZONTAL,
                                        command=self.update_frame)
        self.video_timeline.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # video controls container
        self.video_controls_container = ttk.Frame(self.container)
        self.video_controls_container.pack(side=tk.BOTTOM, pady=(10, 0))

        self.previous_frame_button = ttk.Button(self.video_controls_container, text="⏮", command=self.previous_frame)
        self.previous_frame_button.grid(row=0, column=0, ipadx=self.BUTTON_PADDING, ipady=self.BUTTON_PADDING)

        self.play_pause_button = ttk.Button(self.video_controls_container, text=self.PLAY, command=self.play_pause)
        self.play_pause_button.grid(row=0, column=1, ipadx=self.BUTTON_PADDING, ipady=self.BUTTON_PADDING, padx=10)

        self.next_frame_button = ttk.Button(self.video_controls_container, text="⏭", command=self.next_frame)
        self.next_frame_button.grid(row=0, column=2, ipadx=self.BUTTON_PADDING, ipady=self.BUTTON_PADDING)

        self.current_frame.set(3)

        self.reset_values()

        # window dimensions
        self.window_width = self.video_label.winfo_width()
        self.window_height = self.video_label.winfo_height()

        super().hide()


    def add_media(self, media: list[np.ndarray]):
        """ Adds media to the viewer """
        self.reset_values()

        self.media = media

        # TODO conversion may be necessary

        self.duration = len(self.media)

        self.video_timeline.config(to=self.duration - 1)




    # ################################ GENERAL METHODS ################################ #

    def update_frame(self, event=None):
        """ updates currently displayed frame to scale bar value"""
        frame = self.media[self.current_frame.get()]
        if isinstance(frame, np.ndarray):
            # convert numpy array to PIL Image
            if frame.ndim == 2:
                image = Image.fromarray(frame)
            elif frame.ndim == 3:
                if frame.shape[2] == 1:
                    image = Image.fromarray(frame.squeeze(-1))
                else:
                    image = Image.fromarray(frame)
            else:
                raise ValueError("Unsupported image shape: {}".format(frame.shape))
        else:
            image = frame  # Assume already PIL Image

        # get current label size
        self.video_label.update_idletasks()
        label_width = self.video_label.winfo_width()
        label_height = self.video_label.winfo_height()

        # if label size is not yet set, use default window size
        if label_width <= 1 or label_height <= 1:
            label_width = self.window_width if self.window_width > 1 else 400
            label_height = self.window_height if self.window_height > 1 else 400

        # resize image to fit inside label, preserving aspect ratio
        img_width, img_height = image.size
        scale = min(label_width / img_width, label_height / img_height)
        new_size = (max(1, int(img_width * scale)), max(1, int(img_height * scale)))
        resized_image = image.resize(new_size, Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(resized_image)
        self.video_label.config(image=tk_image)
        self.video_label.image = tk_image


    def play_pause(self):
        """ updates play pause button and playback """
        self.playing_now = not self.playing_now

        if self.playing_now:
            self.play_pause_button.config(text=self.PAUSE)
            self.play_video()
        else:
            self.play_pause_button.config(text=self.PLAY)


    def play_video(self):
        """ Plays image series as a video """
        if self.playing_now:
            self.next_frame()
            self.container.after(self.DELAY, self.play_video)


    def next_frame(self):
        """ Changes image to next frame """
        self.current_frame.set((self.current_frame.get() + 1) % self.duration)
        self.update_frame()


    def previous_frame(self):
        """ Changes image to previous frame """
        self.current_frame.set((self.current_frame.get() - 1) % self.duration)
        self.update_frame()


    def reset_values(self):
        """ Resets video toggle values to default """
        self.media = None
        self.current_frame.set(0)
        self.duration = self.DEFAULT_DURATION


    def show_media(self, images: list[np.ndarray]):
        """ Shows the media viewer with the given images """
        super().show()

        self.video_label.pack(fill=tk.BOTH, expand=True)

        self.video_label.update_idletasks()
        self.add_media(images)

        self.update_frame()
