"""
shopping_menu.py

Configure MarcoNeo's shopping page.
"""

#-------------------------------------------------------------------#

from src.interface.menus.shopping.left.left_grid import LeftGrid
from src.interface.menus.shopping.right.right_grid import RightGrid
from src.utils.gui_utils import Frame, Label

#-------------------------------------------------------------------#

class ShoppingMenu(Frame):
    """
    Menu for the shopping page.
    """
    def __init__(self, gui=None) -> None:
        super().__init__(gui)
        self.gui = gui
        self.grid_propagate(False)

        self.refill_bool = False

        # Setup the left grid for the navbar
        self.left_grid = LeftGrid(self)
        self.left_grid.grid(row=0, column=0, sticky="nsew")

        # Setup the right grid for the header, body and footer
        self.right_grid = RightGrid(self)
        self.right_grid.grid(row=0, column=1, sticky="nsew")

        # Setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

    def retrieve_shopping_items(self, product_type:str) -> list:
        """
        Retrieves the items to display for a product_type given.
        """
        products = []
        for objet in self.gui.app.config.loaded_config:
            if objet["product_type"] == product_type:
                products = objet["products"]
        return products

    def refill_security(self):
        """
        If the current user isn't an admin,
        then an error message is displayed and,
        asks the user to scan an admin card.
        """
        if self.refill_bool:
            self.display_refill()
        else:
            Label(self.right_grid.body, image=self.gui.refill_lbl,
            bg="black").place(relx=0.5, rely=0.5, anchor="center")

    def display_refill(self):
        """
        Displays the refill page.
        """
        self.right_grid.body.clear_body()
        items_to_display = self.retrieve_shopping_items("Rechargement")
        self.right_grid.body.display_items(items_to_display)
