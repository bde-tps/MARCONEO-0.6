"""
header.py

Top section of the shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Frame, ImageButton, Label
from src.interface.widgets.member_card import MemberCard

#-------------------------------------------------------------------#


class Header(Frame):
    """
    Top section of the shopping menu.
    """
    def __init__(self, manager=None) -> None:
        super().__init__(manager)
        self.manager = manager
        self.shopping_manager = manager.manager
        self.loggers = self.shopping_manager.gui.loggers
        self.propagate(True)
        self.configure(bg="#000000", borderwidth=5, border=5,
                        highlightbackground="#4d88ff", highlightthickness=5)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.id_card = Label(self, image=self.shopping_manager.gui.id,
                             bg="#000000", borderwidth=0, highlightthickness=0)

        self.member_card = MemberCard(self)
        self.member_card.place(relx=0.5, rely=0.5, anchor="center")

        self.price_modifier_btn = ImageButton(self,
                                              image=self.shopping_manager.gui.pricemodifier,
                                              command=self.modify_prices)
        self.price_modifier_btn.place(relx=0.88, rely=0.5, anchor="e")

        self.logout_btn = ImageButton(self,
                                      image=self.shopping_manager.gui.logout,
                                      command=self.logout)
        self.logout_btn.place(relx=0.98, rely=0.5, anchor="e")

    def logout(self) -> None:
        """
        Log out the current user and update the page.
        """
        try:
            self.shopping_manager.right_grid.footer.confirm_frame.place_forget()
        except AttributeError:
            pass

        self.shopping_manager.gui.app.cart.reset()
        self.shopping_manager.gui.app.update_user()
        footer =  self.shopping_manager.right_grid.footer
        self.manager.manager.gui.app.current_user.logout()
        self.shopping_manager.right_grid.body.update_body(
            self.shopping_manager.left_grid.navbar.current_toggle)
        footer.reset()
        footer.confirm_btn.configure(text="Confirm", command=footer.confirm_purchase)

        self.loggers.log.info("User logged out.")

    def modify_prices(self):
        """
        Opens the price modifier menu.
        """
        self.shopping_manager.right_grid.price_modifier.show()
        self.loggers.log.info("Price modifier menu opened.")
