"""
LeftGrid.py

Container of the navbar of the shopping page.
"""

#-------------------------------------------------------------------#

from src.interface.menus.shopping.left.navbar import Navbar
from src.utils.gui_utils import Frame

#-------------------------------------------------------------------#


class LeftGrid(Frame):
    """
    Container of the navbar of the shopping page.
    """
    def __init__(self, manager=None):
        super().__init__(manager)
        self.manager = manager
        self.grid_propagate(False)

        self.navbar = Navbar(self)
        self.navbar.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
