"""
app_label.py

Custom label class used in the application's GUI.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Label

#-------------------------------------------------------------------#

class AppLabel(Label):
    """
    Custom label class used in the application's GUI.
    """
    DARK = "#000000"
    DARKGRAY = "#333333"
    GRAY = "#555555"
    LIGHTGRAY = "#777777"
    LIGHT = "#EEEEEE"
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.master = master
        self.config(bg=self.DARK, fg=self.LIGHT,
                    border=0, borderwidth=0)
        if kwargs:
            self.config(**kwargs)
