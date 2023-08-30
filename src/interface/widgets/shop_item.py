"""
ShopItem.py

Configures the items that can be bought in the shop.
"""

#-------------------------------------------------------------------#

import decimal
from src.utils.gui_utils import AppLabel, Frame

#-------------------------------------------------------------------#

class ShopItem(Frame):
    """
    Describes an item that can be bought in the shop.
    """
    def __init__(self, title, price, id_product, manager=None, color:str="#555555"):
        """
        Item's constructor.
        """
        super().__init__(manager)
        self.configure(bg=color, width=120, height=120,
                       highlightbackground=self.darken(color), highlightthickness=6)
        self.color = color
        manager = manager.master
        self.manager = manager
        self.gui_manager = self.manager.manager.manager.gui
        self.cart = self.gui_manager.app.cart
        self.footer = self.manager.manager.footer

        self.title = title
        self.id_product = id_product
        self.price = decimal.Decimal(price)
        self.amount = 0

        self.name_label = None
        self.amount_label = None
        self.price_label = None

        self.setup_container()

    def setup_container(self):
        """
        Defines the container of the item.
        """
        # The name and the amount are labels inside the Frame.
        self.name_label = AppLabel(self, text=self.title.capitalize(), font=("system", 12, "bold"),
                                   fg=self.darken(self.color), bg=self.color)
        self.amount_label = AppLabel(self, text=self.amount, font=("system", 10),
                                     fg=self.darken(self.color), bg=self.color)
        self.price_label = AppLabel(self, text=str(self.price)+"€",
                                    font=("system", 12, "bold"),
                                    fg=self.darken(self.color), bg=self.color)

        self.name_label.place(relx=0.5, rely=0.2, anchor="center")
        self.amount_label.place(relx=0.5, rely=0.5, anchor="center")
        self.price_label.place(relx=0.5, rely=0.8, anchor="center")

        # Binds to the whole widget
        self.bind("<Button-1>", self.add_item)
        for children in self.winfo_children():
            children.bind("<Button-1>", self.add_item)

    def add_item(self, _event=None):
        """
        Adds one to the amount of the item.
        The amount is increased by one inside the body of ShoppingMenu.
        The item is added to the cart. The footer's total label is actualized.
        """
        if self.manager.manager.manager.gui.app.current_user.card_id is None:
            return

        # Cart's modification
        self.amount += 1
        self.cart.add_to_cart({self.id_product: (self.amount, self.price)})
        self.cart.total += self.price

        # Body's modification
        self.amount_label.configure(text=self.amount)

        # Footer's modification
        self.footer.update_footer()

    def darken(self, color: str) -> str:
        """
        Darkens the color.
        """
        factor = 0.5
        red, green, blue = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        red_darkened = int(red * factor)
        green_darkened = int(green * factor)
        blue_darkened = int(blue * factor)
        return f"#{format(red_darkened, '02x')}{format(green_darkened, '02x')}{format(blue_darkened, '02x')}"


    def __repr__(self) -> str:
        return self.title
