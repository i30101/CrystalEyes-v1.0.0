"""
Andrew Kim

27 June 2025

Version 1.0.0

Graphical user interface for CrystalEyes app
"""

import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk

import os
from ctypes import windll
import numpy as np
from PIL import Image
import time

from src.link.analysis import Analysis
from src.media.viewer import Viewer
from src.variables import Variables

from src.nav.nav1 import Nav1
from src.nav.nav2 import Nav2
from src.nav.nav3 import Nav3
from src.nav.nav4 import Nav4

# components
from src.components.console import Console
from src.options import Options

# data boxes
from src.data.pathviewer import PathViewer
from src.data.datatable import DataTable
from src.data.datagraph import DataGraph
from src.data.analyze import AnalyzeBox

from src.link.reader import LinkamDataReader


windll.shcore.SetProcessDpiAwareness(1)



class Gui:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x800")
        self.root.title(Variables.APP_NAME)

        self.options = Options()

        self.linkam_data_file = None

        # ########################## MAIN PANED WINDOW ########################## #
        self.main_paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned_window.pack(fill=tk.BOTH, expand=True)

        # ################################ LEFT COLUMN ################################ #
        self.left_column = ttk.Frame(self.main_paned_window)
        self.main_paned_window.add(self.left_column, weight=1)
        self.left = ttk.Frame(self.left_column)
        self.left.pack(fill=tk.BOTH, expand=True, padx=(20, 10), pady=20)


        # ################ TABS ################ #
        self.tab_control = ttk.Notebook(self.left)

        self.nav1 = Nav1(self.tab_control)
        self.nav2 = Nav2(self.tab_control)
        self.nav3 = Nav3(self.tab_control)
        self.nav4 = Nav4(self.tab_control, self.theme_updated)

        self.tab_control.add(self.nav1, text="File")
        self.tab_control.add(self.nav2, text="Scale")
        self.tab_control.add(self.nav3, text="Data")
        self.tab_control.add(self.nav4, text="Settings")

        self.tab_control.pack(fill=tk.X, pady=Variables.NOPAD_PAD, expand=False)


        # ################ PANED WINDOW ################ #
        self.paned_window = ttk.PanedWindow(self.left, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # media panel
        self.media_frame = ttk.Frame(self.paned_window, height=1, padding=(0, 10))
        self.paned_window.add(self.media_frame, weight=10)
        self.media = Viewer(self.media_frame, self.open_file)
        self.media.clear_media()

        # console
        self.console_frame = ttk.Frame(self.paned_window, height=1)
        self.paned_window.add(self.console_frame, weight=1)
        self.console = Console(self.console_frame)


        # ################################ RIGHT COLUMN ################################ #
        self.right_column = ttk.Frame(self.main_paned_window)
        self.main_paned_window.add(self.right_column, weight=1)
        self.right = ttk.Frame(self.right_column)
        self.right.pack(fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)


        # ################ DATA BOXES ################ #
        self.path_viewer = PathViewer(self.right)
        self.data_table = DataTable(self.right)
        self.data_graph = DataGraph(self.right, self.frame_changed)
        self.analyze_box = AnalyzeBox(self.right)


        self.config_event_entries()

        sv_ttk.set_theme(self.options.get_theme())

        # Set initial pane sizes based on LEFT_WIDTH and RIGHT_WIDTH
        self.root.update_idletasks()
        total_width = self.root.winfo_width()
        left_width = int(total_width * Variables.LEFT_WIDTH)
        self.main_paned_window.sashpos(0, left_width)

        if self.options.get_open_fullscreen():
            self.root.after(100, lambda: self.root.state('zoomed'))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        # run GUI
        self.root.mainloop()


    def config_event_entries(self):
        """ Configures events and entries """

        # tab control configs
        self.nav1.open_file_button.config(command=self.open_file)
        self.nav1.clear_button.config(command=self.clear_media)

        # tab 2 configs
        self.nav2.reset_scale_button.config(command=self.reset_scale)
        self.set_px_entry(self.options.get_px())
        self.nav2.px_input.trace_add('write', self.px_entry_updated)
        self.set_um_entry(self.options.get_um())
        self.nav2.um_input.trace_add('write', self.um_entry_updated)
        self.set_scale_entry(self.options.get_scale())
        self.nav2.scale_input.trace_add('write', self.scale_entry_updated)

        # tab 3 configs
        self.nav3.browse_button.config(command=self.folder_browse)
        self.nav3.export_path.set(self.options.get_export_path())
        self.nav3.export_path.trace_add('write', self.export_path_updated)
        self.nav3.processed_images.set(self.options.get_processed_checkbox())
        self.nav3.processed_images.trace_add(
            'write',
            lambda *_: self.options.set_open_fullscreen(self.nav3.processed_images.get())
        )
        self.nav3.raw_images.set(self.options.get_raw_checkbox())
        self.nav3.raw_images.trace_add(
            'write',
            lambda *_: self.options.set_raw_checkbox(self.nav3.raw_images.get())
        )
        self.nav3.download_button.config(command=self.export_data)

        # tab 4 configs
        self.nav4.theme_combo.set(self.options.get_theme().capitalize())
        self.nav4.open_fullscreen.set(self.options.get_open_fullscreen())
        self.nav4.open_fullscreen.trace_add(
            'write',
            lambda *_ : self.options.set_open_fullscreen(self.nav4.open_fullscreen.get())
        )
        self.nav4.reset_settings_button.config(command=self.settings_reset)


        # data table configs
        self.media.media_viewer.current_frame.trace_add(
            'write',
            lambda *_: self.frame_changed(self.media.media_viewer.current_frame.get())
        )
        self.data_table.frame_number.trace_add(
            'write',
            self.frame_entry_updated
        )
        self.analyze_box.analyze_button.config(command=self.analyze)




    # ################################ GENERAL METHODS ################################ #

    def on_close(self):
        """ What happens when the GUI window is closed """
        self.options.write_options()
        self.root.destroy()


    def frame_changed(self, next_frame: int):
        """ When the currently displayed frame changes """

        if not isinstance(next_frame, int):
            return

        self.data_table.set_data(*self.linkam_data_file.get_data(next_frame))
        self.media.media_viewer.to_frame(next_frame)



    # ################################ TAB 1 METHODS ################################ #

    def open_file(self):
        """ User opens new LDF file """
        filepath = filedialog.askopenfilename(filetypes=[(
            "Linkam Data Files",
            ".ldf"
        )])

        # if no files were selected, do nothing
        if not filepath:
            return

        self.linkam_data_file = LinkamDataReader.extract_data(filepath)

        self.media.show_media(self.linkam_data_file.raw_images)

        self.path_viewer.set_filepath(self.linkam_data_file.filepath)

        self.data_graph.update_graph(self.linkam_data_file.temperatures)

        # update console
        self.console.update(f"{self.linkam_data_file.filepath} uploaded")


    def clear_media(self):
        """ Clears media """
        self.linkam_data_file = None
        self.media.clear_media()
        self.data_table.clear_data()
        self.data_graph.clear_graph()
        self.path_viewer.clear_filepath()

        self.console.update("Media cleared")


    def theme_updated(self):
        """ Theme was updated """
        self.options.set_theme(self.nav4.theme_combo.get().lower())
        sv_ttk.set_theme(self.options.get_theme())


    def settings_reset(self):
        """ Settings were reset """
        self.options.reset_options()

        sv_ttk.set_theme("light")

        self.nav3.processed_images.set(self.options.get_processed_checkbox())
        self.nav3.raw_images.set(self.options.get_raw_checkbox())
        self.nav3.export_path.set(self.options.get_export_path())

        self.nav4.theme_combo.set(self.options.get_theme().capitalize())
        self.nav4.open_fullscreen.set(self.options.get_open_fullscreen())

        self.set_scale_entry(self.options.get_scale())
        self.set_px_entry(self.options.get_px())
        self.set_um_entry(self.options.get_um())

        self.console.update("Settings reset to default")



    # ################################ TAB 2 METHODS ################################ #

    def reset_scale(self):
        """ Resets displayed scale in Scale tab """
        self.set_scale_entry(Variables.DEFAULT_SCALE)
        self.set_px_entry(Variables.DEFAULT_PX)
        self.set_um_entry(Variables.DEFAULT_UM)


    def get_input_values(self) -> tuple:
        """ Gets all input values and tries to convert to float """
        return (float(self.nav2.scale_input.get()),
                float(self.nav2.px_input.get()),
                float(self.nav2.um_input.get()))


    def set_scale_entry(self, scale: float):
        """ Sets value in scale entry, always rounds to 5 decimal points"""
        if scale == self.nav2.scale_input.get():
            return
        new_scale = round(scale, 5)
        self.nav2.scale_input.set(new_scale)
        Analysis.set_scale(float(self.nav2.scale_entry.get()))


    def set_px_entry(self, px: float):
        """ Sets value in pixel entry """
        if px == self.nav2.scale_input.get():
            return
        new_px = round(px, 3)
        self.nav2.px_input.set(new_px)


    def set_um_entry(self, um: float):
        """ Sets value in um entry """
        if um == self.nav2.scale_input.get():
            return
        self.nav2.um_input.set(um)


    def scale_entry_updated(self, _1, _2, _3):
        """ Callback for update to scale entry """
        try:
            inputs = self.get_input_values()
        except ValueError:
            self.console.error("non-integer character in scale input")
            return
        if 0 in inputs:
            self.console.error("zero in scale input")
            return
        self.set_px_entry(inputs[2] / inputs[0])
        self.options.set_scale(inputs[0])
        Analysis.set_scale(inputs[0])


    def px_entry_updated(self, _1, _2, _3):
        """ Callback for update to px entry """
        try:
            inputs = self.get_input_values()
        except ValueError:
            self.console.error("non-integer character in px input")
            return
        if 0 in inputs:
            self.console.error("zero in px input")
            return
        self.set_scale_entry(inputs[2] / inputs[1])
        self.options.set_px(inputs[1])


    def um_entry_updated(self, _1, _2, _3):
        """ Callback for update to um entry """
        try:
            inputs = self.get_input_values()
        except ValueError:
            self.console.error("non-integer character in μm entry")
            return
        if 0 in inputs:
            self.console.error("zero in μm input")
            return
        self.set_scale_entry(inputs[2] / inputs[1])
        self.options.set_um(inputs[2])



    # ################################ TAB 3 METHODS ################################ #

    def folder_browse(self):
        """ User sets folder to export data """
        filepath = filedialog.askdirectory()
        if len(filepath) == 0:
            return
        self.nav3.export_path.set(filepath)



    def export_path_updated(self, _1, _2, _3):
        """ Path to which data is exported is updated """
        self.options.set_export_path(self.nav3.export_path.get())


    def export_data(self):
        """ User wants to export data """

        if self.linkam_data_file is None:
            self.console.error("No LDF file loaded")
            return

        if not self.linkam_data_file.processed_images:
            self.console.error("File not analyzed yet")

        export_directory = (self.nav3.export_path.get() + "/" +
                            self.linkam_data_file.filepath[ : self.linkam_data_file.filepath.rfind(".ldf")] + "/")

        # ensure the folder directory exists before writing
        os.makedirs(export_directory, exist_ok=True)

        # export analysis data
        data_df = self.linkam_data_file.to_df()
        data_df.to_excel(export_directory + self.linkam_data_file.filepath + ".xlsx", index=False)

        # export
        areas_df = self.linkam_data_file.area_to_df()
        areas_df.to_excel(export_directory + self.linkam_data_file.filepath + "_areas.xlsx", index=False)

        if self.nav3.raw_images.get():
            # export raw images to directory "raw"
            raw_dir = os.path.join(export_directory, "raw")
            os.makedirs(raw_dir, exist_ok=True)
            for i, img in enumerate(self.linkam_data_file.raw_images):
                pil_img = Image.fromarray(img)
                pil_img.save(os.path.join(raw_dir, f"raw_{i:04d}.jpg"), "JPEG")

        if self.nav3.processed_images.get():
            # export processed images to directory "processed"
            processed_dir = os.path.join(export_directory, "processed")
            os.makedirs(processed_dir, exist_ok=True)
            for i, img in enumerate(self.linkam_data_file.processed_images):
                pil_img = Image.fromarray(img)
                pil_img.save(os.path.join(processed_dir, f"processed_{i:04d}.jpg"), "JPEG")

        self.console.update(f"Data export to {export_directory} successful")




    # ################################ DATA BOX METHODS ################################ #

    def frame_entry_updated(self, _1, _2, _3):
        """ Callback for frame entry update """

        if self.linkam_data_file is None:
            return

        try:
            frame_number = int(self.data_table.frame_number.get())
        except (ValueError, tk.TclError):
            self.console.error("non-integer character in frame number input")
            return

        if frame_number < 0 or frame_number >= len(self.linkam_data_file.raw_images):
            self.console.error("frame number out of bounds")
            return

        self.frame_changed(self.data_table.frame_number.get())


    def analyze(self):
        """ User wants to analyze LDF file """

        if self.linkam_data_file is None:
            self.console.error("No LDF file loaded")
            return

        start_frame = self.analyze_box.starting_frame.get()
        end_frame = self.analyze_box.ending_frame.get() + 1

        if (start_frame < 0
                or end_frame > len(self.linkam_data_file.raw_images)
                or start_frame == end_frame
                or start_frame > end_frame ):
            self.console.error("Frame range out of bounds")
            return

        self.linkam_data_file = self.linkam_data_file.trim(
            start_frame,
            end_frame
        )

        t0 = time.time()
        self.linkam_data_file.analyze()
        t1 = time.time()
        duration = t1 - t0

        self.media.show_media(self.linkam_data_file.processed_images)
        self.data_graph.update_graph(self.linkam_data_file.temperatures)
        self.console.message(
            self.linkam_data_file.data_summary()
            + f"\n    Total duration: {duration:.3f} seconds"
            + f"({duration / len(self.linkam_data_file.raw_images):.3f} seconds per frame)"
        )
