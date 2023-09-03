"""
footer.py

Describes the footer of the shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Frame, Label, ImageButton

#-------------------------------------------------------------------#

class Footer(Frame):
    """
    Footer of the shopping menu.
    Contains the confirm button and the reset button
    and the total of the cart.
    """
    def __init__(self, manager=None):
        super().__init__(manager)
        self.manager = manager
        self.shopping_manager = manager.manager
        self.loggers = self.shopping_manager.gui.app.loggers
        self.propagate(False)
        self.configure(bg="#000000", borderwidth=5, border=5,
                    highlightbackground="#4d88ff", highlightthickness=5)
        self.cart = self.shopping_manager.gui.app.cart

        self.confirm_popup = None
        self.debiter_lbl = None
        self.debiter_total = None

        self.footer_frame = Frame(self, bg="black")
        self.footer_frame.pack(fill="both", expand=True)

        self.setup_container()

    def setup_container(self):
        """
        Sets up the container of the footer.
        """
        self.confirm_btn = ImageButton(self.footer_frame, image=self.shopping_manager.gui.confirm,
                                       command=self.confirm_purchase)

        self.back_btn = ImageButton(self, image=self.manager.manager.gui.back,
                                  command=lambda: self.manager.manager.gui.change_menu(
                                      self.manager.manager.gui.main_menu))

        self.confirm_frame = Frame(self, bg="black")
        self.confirm_lbl = Label(self.confirm_frame, image=self.shopping_manager.gui.confirm_lbl,
                                    bg="black", highlightthickness=0, borderwidth=0)
        self.cancel_btn = ImageButton(self.confirm_frame, image=self.shopping_manager.gui.cancel,
                                        command=self.cancel_purchase)
        self.cancel_btn.pack(side="left", padx=5)
        self.confirm_lbl.pack(side="left", padx=5)


        cart_frame = Frame(self.footer_frame, bg="black")
        self.cart_img = Label(cart_frame, image=self.shopping_manager.gui.cart,
                              bg="black", border=0,
                              borderwidth= 0, highlightthickness=0)
        self.total_label = Label(cart_frame, text=f"{self.cart.total} €",
                                 font=("System", 20, "bold"), bg="black", fg="white")
        self.cart_img.pack(side="left", padx=10)
        self.total_label.pack(side="left", padx=10)

        cart_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.back_btn.place(relx=0.02, rely=0.5, anchor="w")
        self.confirm_btn.place(relx=0.98, rely=0.5, anchor="e")

    def reset(self):
        """
        Reset the page.
        """
        if not self.cart.total:
            return
        self.cart.reset()
        self.update_footer()
        self.shopping_manager.right_grid.body.update_body(
            self.shopping_manager.left_grid.navbar.current_toggle)

    def update_footer(self):
        """
        Updates the total label.
        """
        self.total_label.configure(text=f"{self.cart.total} €")

        # If the cart is empty, the back button is displayed.
        # Else, the discard button is displayed.
        if not self.cart.total:
            self.back_btn.configure(image=self.manager.manager.gui.back,
            command=lambda: self.manager.manager.gui.change_menu(
                self.manager.manager.gui.main_menu))
        else:
            self.back_btn.configure(image=self.manager.manager.gui.discard,
            command=self.reset)

        if self.shopping_manager.gui.app.current_user.balance is None:
            return

        # If the user is recharging, the total label is not altered.
        if self.manager.manager.left_grid.navbar.current_toggle == "Rechargement":
            return

        # If the user doesn't have enough money, the total label is red.
        if self.cart.total>self.shopping_manager.gui.app.current_user.balance:
            self.total_label.configure(fg="red")
        else:
            self.total_label.configure(fg="white")

    def confirm_purchase(self):
        """
        Confirms the purchase.
        """
        if not self.cart.total:
            return

        if self.shopping_manager.left_grid.navbar.current_toggle != "Rechargement":
            if self.shopping_manager.gui.app.current_user.balance < self.cart.total:
                self.loggers.log.warning("Not enough money to purchase.")
                return

        for widget in self.manager.manager.left_grid.navbar.winfo_children():
            widget.configure(state="disabled")

        for widget in self.manager.body.frame.winfo_children():
            widget.destroy()

        # Popup displayed when confirming a purchase.
        debiter_lbl = Label(self.manager.body.frame,
                            bg="black", highlightthickness=0, borderwidth=0)
        if self.shopping_manager.gui.app.cart.total>0:
            debiter_lbl.configure(image=self.shopping_manager.gui.debiter)
        else:
            debiter_lbl.configure(image=self.shopping_manager.gui.recharger_lbl)

        debiter_total = Label(self.manager.body.frame,
                                   text=f"{self.shopping_manager.gui.app.cart.total} €",
                                    font=("System", 40, "bold"), bg="black", fg="gold")

        debiter_lbl.grid(row=0, column=0, columnspan=2, pady=5)
        debiter_total.grid(row=1, column=0, columnspan=2, pady=5)

        self.confirm_frame.place(relx=0.43, rely=0.5, anchor="center")
        self.confirm_btn.configure(command=self.do_purchase)

    def cancel_purchase(self):
        """
        Cancels the purchase.
        """
        for widget in self.manager.body.frame.winfo_children():
            widget.destroy()

        for widget in self.manager.manager.left_grid.navbar.winfo_children():
            widget.configure(state="normal")

        self.confirm_frame.place_forget()
        self.manager.body.update_body(self.shopping_manager.left_grid.navbar.current_toggle)
        self.confirm_btn.configure(command=self.confirm_purchase)
        self.reset()

    def do_purchase(self):
        """
        Does the purchase.
        """
        self.manager.body.frame.place_forget()
        self.confirm_frame.place_forget()
        for widget in self.manager.manager.left_grid.navbar.winfo_children():
            widget.configure(state="normal")

        self.shopping_manager.gui.app.payment_service.purchase()
        self.shopping_manager.gui.app.cart.reset()
        self.loggers.log.debug("Cart has been reset.")
        self.shopping_manager.gui.app.update_user()
        self.shopping_manager.right_grid.body.update_body(
            self.shopping_manager.left_grid.navbar.current_toggle)
        self.reset()
        self.confirm_btn.configure(command=self.confirm_purchase)
