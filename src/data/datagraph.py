"""
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables

# Add matplotlib imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataGraph:
    """ Data graph for visualizing temperature"""

    def __init__(self, root, on_dot_click: callable = None):
        self.root = root

        # TODO see if this can be moved to gui
        self.on_dot_click = on_dot_click

        # create a bordered box
        self.box = ttk.LabelFrame(self.root, text="Temperature", padding=(10, 10))
        self.box.grid(row=0, column=0, padx=10, pady=Variables.NOPAD_PAD, sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)

        # Matplotlib Figure and Canvas
        self.figure = Figure(figsize=(5, 3), dpi=80)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.box)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.temperature_data = []
        self.dot_artists = []

        # Connect matplotlib pick event for dot clicks
        self.figure.canvas.mpl_connect('pick_event', self.on_dot_click)

    def update_graph(self, temperature_data):
        """
        Update the graph with new temperature data.
        temperature_data: list of floats (temperatures per frame)
        """
        self.clear_graph()
        if not temperature_data:
            return

        self.temperature_data = temperature_data
        frames = list(range(len(temperature_data)))

        self.ax.clear()
        self.ax.set_title("Temperature")
        self.ax.set_xlabel("Frame")
        self.ax.set_ylabel("Temp")

        # Plot line
        self.ax.plot(frames, temperature_data, color="gray", linewidth=2)

        # Plot dots with picker enabled
        self.dot_artists = self.ax.scatter(frames, temperature_data, color="blue", edgecolors="black", s=40, picker=5)

        # Set axis limits and labels
        self.ax.set_xlim(0, max(frames) if frames else 1)
        if temperature_data:
            self.ax.set_ylim(min(temperature_data), max(temperature_data))
            self.ax.text(frames[0], max(temperature_data), f"Max {max(temperature_data):.1f}", va='bottom', ha='left')
            self.ax.text(frames[0], min(temperature_data), f"Min {min(temperature_data):.1f}", va='top', ha='left')

        self.canvas.draw()

    def clear_graph(self):
        """Clear the graph."""
        self.ax.clear()
        self.canvas.draw()
        self.temperature_data = []
        self.dot_artists = []

    def _on_canvas_click(self, event):
        """Handle click on canvas, check if a dot was clicked."""
        for frame, temp, x, y, dot_id in self.data_points:
            dx = event.x - x
            dy = event.y - y
            if dx * dx + dy * dy <= self.dot_radius * self.dot_radius:
                if self.on_dot_click:
                    self.on_dot_click(frame)
                break

