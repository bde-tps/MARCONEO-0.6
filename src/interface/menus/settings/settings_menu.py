"""
settings_menu.py

Configure MarcoNeo's settings page.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import AppFrame
from src.interface.menus.settings.left.left_sett import LeftSett
from src.interface.menus.settings.right.right_sett import RightSett

#-------------------------------------------------------------------#

class SettingsMenu(AppFrame):
    """
    MarcoNeo's settings page.

    Contains the settings of the application:
    Fouaille will be able to config the items
    they want to see in the shopping menu.
    """
    def __init__(self, gui=None) -> None:
        super().__init__(gui)
        self.gui = gui
        self.propagate(False)

        # Setup the left grid for the navbar
        self.left_grid = LeftSett(self)
        self.left_grid.grid(row=0, column=0, sticky="nsew")

        # Setup the right grid for the header, body and footer
        self.right_grid = RightSett(self)
        self.right_grid.grid(row=0, column=1, sticky="nsew")

        # Setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

    def retrieve_settings_items(self, toggle):
        """
        Retrieves from api_config.json the items
        following the toggle.
        """
        data = self.gui.app.config.api_config.config_json
        items = []
        for menu in data:
            if menu["product_type"] == toggle:
                items = menu["products"]
                break
        return items

    def refresh(self):
        """
        Refreshes the settings page.
        """
        self.gui.app.config.api_config.setup_jsons()
        self.right_grid.body.update_body(self.left_grid.navbar.current_toggle)
