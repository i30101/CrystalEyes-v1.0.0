"""
Andrew Kim

27 June 2025

Version 1.0.0

Graphical user interface for CrystalEyes app
"""

import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk

from ctypes import windll

from src.media.viewer import Viewer
from src.variables import Variables

from src.nav.nav1 import Nav1
from src.nav.nav2 import Nav2
from src.nav.nav3 import Nav3

# components
from src.components.console import Console
from src.options import Options

# data boxes
from src.data.pathviewer import PathViewer
from src.data.datatable import DataTable
from src.data.datagraph import DataGraph
from src.data.analyze import AnalyzeBox
from src.data.ramp import RampBox

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

        self.tab1 = Nav1(self.tab_control)
        self.tab2 = Nav2(self.tab_control)
        self.tab3 = Nav3(self.tab_control)

        self.tab_control.add(self.tab1, text="File")
        self.tab_control.add(self.tab2, text="Scale")
        self.tab_control.add(self.tab3, text="Data")

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
        # TODO maybe change size of data graph
        self.analyze_box = AnalyzeBox(self.right)
        # self.ramp_box = RampBox(self.right)



        self.config_event_entries()

        sv_ttk.set_theme(self.options.get_theme())

        # self.root.after(100, lambda: self.root.state('zoomed'))
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        # run GUI
        self.root.mainloop()


    def config_event_entries(self):
        """ Configures events and entries """

        # tab control configs
        self.tab1.open_file_button.config(command=self.open_file)
        self.tab1.clear_button.config(command=self.clear_media)
        self.tab1.theme_button.config(command=self.theme_updated)
        self.tab1.reset_settings_button.config(command=self.settings_reset)

        # tab 2 configs
        self.tab2.reset_scale_button.config(command=self.reset_scale)
        self.set_px_entry(self.options.get_px())
        self.tab2.px_input.trace_add('write', self.px_entry_updated)
        self.set_um_entry(self.options.get_um())
        self.tab2.um_input.trace_add('write', self.um_entry_updated)
        self.set_scale_entry(self.options.get_scale())
        self.tab2.scale_input.trace_add('write', self.scale_entry_updated)

        # tab 3 configs
        self.tab3.browse_button.config(command=self.folder_browse)
        self.tab3.export_path.set(self.options.get_export_path())
        self.tab3.export_path.trace_add('write', self.export_path_updated)
        self.tab3.processed_images.set(self.options.get_processed_checkbox())
        self.tab3.processed_images.trace_add(
            'write',
            lambda *_: self.options.set_processed_checkbox(self.tab3.processed_images.get())
        )
        self.tab3.raw_images.set(self.options.get_raw_checkbox())
        self.tab3.raw_images.trace_add(
            'write',
            lambda *_: self.options.set_raw_checkbox(self.tab3.raw_images.get())
        )
        self.tab3.download_button.config(command=self.export_data)

        # video configs
        self.media.media_viewer.current_frame.trace_add(
            'write',
            lambda *_: self.frame_changed(self.media.media_viewer.current_frame.get())
        )
        self.data_table.frame_number.trace_add(
            'write',
            self.frame_entry_updated
        )




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

        # TODO call additional methods

        self.linkam_data_file = LinkamDataReader.extract_data(filepath)

        self.media.show_media(self.linkam_data_file.raw_images)

        self.path_viewer.set_filepath(self.linkam_data_file.filepath)

        self.data_graph.update_graph(self.linkam_data_file.temperatures)

        # update console
        self.console.update(f"{self.linkam_data_file.filepath} uploaded")


    def clear_media(self):
        """ Clears media """
        # TODO call additional methods
        self.media.clear_media()
        self.data_table.clear_data()
        self.data_graph.clear_graph()
        self.path_viewer.clear_filepath()

        self.console.message("Media cleared")


    def theme_updated(self):
        """ Theme was updated """
        if self.options.get_theme() == "light":
            self.options.set_theme("dark")
        elif self.options.get_theme() == "dark":
            self.options.set_theme("light")
        sv_ttk.set_theme(self.options.get_theme())


    def settings_reset(self):
        """ Settings were reset """
        self.options.reset_options()

        sv_ttk.set_theme("light")

        self.tab3.processed_images.set(self.options.get_processed_checkbox())
        self.tab3.raw_images.set(self.options.get_raw_checkbox())
        self.tab3.export_path.set(self.options.get_export_path())

        self.set_scale_entry(self.options.get_scale())
        self.set_px_entry(self.options.get_px())
        self.set_um_entry(self.options.get_um())

        # TODO add more methods

        self.console.message("Settings reset to default")



    # ################################ TAB 2 METHODS ################################ #

    def reset_scale(self):
        """ Resets displayed scale in Scale tab """
        self.set_scale_entry(Variables.DEFAULT_SCALE)
        self.set_px_entry(Variables.DEFAULT_PX)
        self.set_um_entry(Variables.DEFAULT_UM)


    def get_input_values(self) -> tuple:
        """ Gets all input values and tries to convert to float """
        return (float(self.tab2.scale_input.get()),
                float(self.tab2.px_input.get()),
                float(self.tab2.um_input.get()))


    def set_scale_entry(self, scale: float):
        """ Sets value in scale entry, always rounds to 5 decimal points"""
        if scale == self.tab2.scale_input.get():
            return
        new_scale = round(scale, 5)
        self.tab2.scale_input.set(new_scale)
        # TODO update this
        # Analysis.set_scale(float(self.tab2.scale_entry.get()))


    def set_px_entry(self, px: float):
        """ Sets value in pixel entry """
        if px == self.tab2.scale_input.get():
            return
        new_px = round(px, 3)
        self.tab2.px_input.set(new_px)


    def set_um_entry(self, um: float):
        """ Sets value in um entry """
        if um == self.tab2.scale_input.get():
            return
        self.tab2.um_input.set(um)


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
        self.tab3.export_path.set(filepath)



    def export_path_updated(self, _1, _2, _3):
        """ Path to which data is exported is updated """
        self.options.set_export_path(self.tab3.export_path.get())


    def export_data(self):
        """ User wants to export data """
        # TODO update this
        pass


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

        if frame_number < 0 or frame_number >= self.linkam_data_file.length:
            self.console.error("frame number out of bounds")
            return

        self.frame_changed(self.data_table.frame_number.get())
