"""
right_sett.py

Right side of the setting page of the app.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Frame
from src.interface.menus.settings.right.sett_header import SettHeader
from src.interface.menus.settings.right.sett_body import SettBody

#-------------------------------------------------------------------#

class RightSett(Frame):
    """
    Container of the header, body and footer of the shopping page.
    """
    def __init__(self, manager=None):
        super().__init__(manager)
        self.manager = manager
        self.grid_propagate(False)

        self.header = SettHeader(self)
        self.header.grid(row=0, column=0, sticky="nsew")
        self.body = SettBody(self)
        self.body.grid(row=1, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
