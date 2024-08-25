"""
Andrew Kim

3 July 2025

Version 1.0.0

Data graph for visualizing temperature
"""


from src.data.databox import DataBox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataGraph(DataBox):
    """ Data graph for visualizing temperature"""

    def __init__(self, root, on_dot_click: callable):
        super().__init__(root, "Temperature")

        self.on_dot_click = on_dot_click

        # Matplotlib Figure and Canvas
        self.figure = Figure(figsize=(5, 3), dpi=80)
        self.figure.subplots_adjust(top=0.9, right=0.97, bottom=0.2)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.box)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.temperature_data = []
        self.dot_artists = []

        # Connect matplotlib pick event for dot clicks
        self.figure.canvas.mpl_connect('pick_event', self.on_canvas_click)

    def update_graph(self, temperature_data):
        """ Update the graph with new temperature data """
        self.clear_graph()
        if not temperature_data:
            return

        self.temperature_data = temperature_data
        frames = list(range(len(temperature_data)))

        self.ax.clear()
        self.ax.set_xlabel("Frame")
        self.ax.set_ylabel("Temp (°C)")

        # Plot line
        self.ax.plot(frames, temperature_data, color="gray", linewidth=2)

        # Plot dots with picker enabled
        self.dot_artists = self.ax.scatter(frames, temperature_data, color="blue", s=30, picker=5)

        # Set axis limits and labels
        self.ax.set_xlim(0, max(frames) if frames else 1)
        if temperature_data:
            self.ax.set_ylim(min(temperature_data), max(temperature_data))

        self.canvas.draw()

    def clear_graph(self):
        """Clear the graph."""
        self.ax.clear()
        self.canvas.draw()
        self.temperature_data = []
        self.dot_artists = []


    def on_canvas_click(self, event):
        """ Handle click on canvas, check if a dot was clicked """
        if hasattr(event, "ind") and event.ind is not None and len(event.ind) > 0:
            idx = event.ind[0]
            if 0 <= idx < len(self.temperature_data):
                frame = idx
                self.on_dot_click(int(frame))
