"""
left_sett.py

Left side of the settings page.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Frame
from src.interface.menus.settings.left.sett_navbar import SettNavbar

#-------------------------------------------------------------------#

class LeftSett(Frame):
    """
    Left side of the settings page.
    """
    def __init__(self, shopping_menu) -> None:
        super().__init__(shopping_menu)
        self.manager = shopping_menu
        self.propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.navbar = SettNavbar(self)
        self.navbar.pack(fill="both", expand=True)
