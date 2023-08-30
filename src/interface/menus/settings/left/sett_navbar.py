"""
sett_navbar.py

Navbar of the settings page of the app.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Frame, AppButton

#-------------------------------------------------------------------#

class SettNavbar(Frame):
    """
    Navbar of the settings page of the app.
    """
    def __init__(self, left_grid=None):
        super().__init__(left_grid)
        self.manager = left_grid
        self.config(bg="#000000")
        self.back_btn = None
        self.product_type = self.manager.manager.gui.app.config.api_config.categories
        self.current_toggle = self.product_type[0]
        self.setup_buttons()

    def setup_buttons(self) -> bool:
        """
        Defines the buttons used in the navbar.
        """
        for i, menu in enumerate(self.product_type):
            button = AppButton(self, text=menu, command=lambda menu=menu: self.toggle(menu))
            setattr(self, f"btn{i}", button)
            button.pack(fill="both", expand=True, side="top", padx=10, pady=10)
        self.back_btn = AppButton(self, text="Back",
                                    command=lambda:
                                        self.manager.manager.gui.change_menu(
                                            self.manager.manager.gui.main_menu))

        self.back_btn.pack(side="bottom", pady=10, padx=10, fill="x")

    def toggle(self, toggle: str) -> None:
        """
        Changes the current toggle of the navbar.
        """
        self.current_toggle = toggle

        # Update button's colors
        for i, menu in enumerate(self.product_type):
            button = getattr(self, f"btn{i}")
            if menu == self.current_toggle:
                button.configure(bg=AppButton.ACTIVE_TOGGLE)  # set active toggle color
            else:
                button.configure(bg=AppButton.DEFAULT_BG)  # set default color

        self.manager.manager.right_grid.body.update_body(toggle)
