"""
price_modifier.py

This menu is made to allow Fouailles to change
the prices of products. Contains a digital keyboard
to enter the new prices.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Frame, ImageButton, LabelLabelPair

#-------------------------------------------------------------------#

class PriceModifier(Frame):
    """
    Price modifier menu.
    """
    def __init__(self, manager=None):
        super().__init__(manager)
        self.manager = manager
        self.shopping_manager = manager.manager
        self.loggers = self.shopping_manager.gui.app.loggers
        self.propagate(False)
        self.configure(bg="#000000", highlightthickness=5,
                            highlightbackground="#2683ff")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Frames
        self.list_frame = Frame(self, bg="#000000")
        self.control_frame = Frame(self, bg="#000000")
        self.reset_frame = Frame(self, bg="#000000")
        self.control_frame.propagate(False)
        self.list_frame.pack(side='left', padx=(115,0), pady=10)
        self.control_frame.pack(side='left', padx=0, pady=10, fill="both", expand=True)

        # Widgets
        self.setup_digital_keyboard()
        enter_button = ImageButton(self.control_frame,
                                   image=self.shopping_manager.gui.priceconfirm,
                                    command=self.on_enter_click)
        back_btn = ImageButton(self.reset_frame,
                               image=self.shopping_manager.gui.back,
                                command=self.back)
        reset_btn = ImageButton(self.reset_frame,
                                image=self.shopping_manager.gui.resetprice,
                                command=self.reset)

        enter_button.place(relx=0.5, rely=0.90, anchor="center")
        reset_btn.pack(side="top", padx=10, pady=(0, 145))
        back_btn.pack(side="top", padx=10, pady=(145, 0))
        self.reset_frame.place(relx=0.08, rely=0.5, anchor="center")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.display_item_list()

    def show(self):
        """
        Shows the price modifier.
        """
        self.pack(side="top", fill="both", expand=True)
        self.manager.columnconfigure(0, weight=1)
        self.manager.rowconfigure(0, weight=1)

    def on_button_click(self, value):
        """
        Handles the button click event.
        """
        focused_widget = self.get_focused_item()
        if focused_widget is None:
            return

        current_text = focused_widget.entry.cget("text")
        if len(current_text) > 4:
            return

        if value == "." and "." in current_text:
            return

        new_text = current_text + str(value)
        focused_widget.entry.configure(text=new_text)

    def on_clear_click(self):
        """
        Clears the digital keyboard.
        """
        focused_widget = self.get_focused_item()
        if focused_widget is None:
            return

        focused_widget.entry.configure(text="")

    def on_enter_click(self):
        """
        Confirms the new price.
        """
        focused_widget = self.get_focused_item()
        if focused_widget is None:
            return

        new_price = focused_widget.entry.cget("text")
        if new_price == "":
            return

        focused_widget.price = new_price
        focused_widget.entry.configure(text=new_price)
        self.change_price_config(focused_widget, new_price)
        self.back()

    def create_digit_button(self, frame, digit):
        """
        Creates a digit button.
        """
        button = ImageButton(frame, image=getattr(self.shopping_manager.gui, f"btn{digit}"),
                        command=lambda: self.on_button_click(digit))
        if digit == 0:
            button.grid(row=3, column=1, columnspan=2)
        elif digit in [7, 8, 9]:
            button.grid(row=0, column=digit-7, pady=5, padx=5)
        elif digit in [4, 5, 6]:
            button.grid(row=1, column=digit-4, pady=5, padx=5)
        elif digit in [1, 2, 3]:
            button.grid(row=2, column=digit-1, pady=5, padx=5)

    def setup_digital_keyboard(self):
        """
        Sets up the digital keyboard.
        """
        keyboard_frame = Frame(self.control_frame, bg="#000000")
        keyboard_frame.place(relx=0.5, rely=0.4, anchor="center", x=0, y=0)

        for digit in range(1, 10):
            self.create_digit_button(keyboard_frame, digit)

        coma_button = ImageButton(keyboard_frame, text=".",
                                  image=self.shopping_manager.gui.dot,
                                command=lambda: self.on_button_click("."))
        coma_button.grid(row=3, column=0, pady=5, padx=5)

        zero_button = ImageButton(keyboard_frame, text="0",
                                  image=self.shopping_manager.gui.btn0,
                                command=lambda: self.on_button_click(0))
        zero_button.grid(row=3, column=1, pady=5, padx=5)

        clear_button = ImageButton(keyboard_frame,
                                   image=self.shopping_manager.gui.backspace,
                                command=self.on_clear_click)
        clear_button.grid(row=3, column=2, pady=5, padx=5)

    def back(self):
        """
        Goes back to the shopping menu.
        """
        # Reset the cart
        self.manager.manager.gui.app.cart.reset()

        # Setup the grid
        self.manager.grid_columnconfigure(0, weight=1)
        self.manager.grid_rowconfigure(0, weight=2)
        self.manager.grid_rowconfigure(1, weight=5)
        self.manager.grid_rowconfigure(2, weight=2)

        self.shopping_manager.right_grid.header.grid(row=0, column=0, sticky='nsew')
        self.shopping_manager.right_grid.body.grid(row=1, column=0, sticky='nsew')
        self.shopping_manager.right_grid.footer.grid(row=2, column=0, sticky='nsew')

        self.shopping_manager.right_grid.body.update_body(
            self.shopping_manager.left_grid.navbar.current_toggle)
        self.loggers.log.debug("Price modifier has been closed.")
        self.pack_forget()

    def display_item_list(self):
        """
        Displays the items in the list.
        """
        # Clear the list
        for child in self.list_frame.winfo_children():
            child.destroy()

        current_toggle = self.shopping_manager.left_grid.navbar.current_toggle
        items = self.shopping_manager.retrieve_shopping_items(current_toggle)

        # Display the items
        for item in items:
            LabelLabelPair(self.list_frame,
                           name=item["name"],
                           price=str(item["price"]),
                           color=item["color"]).pack(fill="both", expand=True,
                                                          side="top", padx=5, pady=5)

    def get_focused_item(self):
        """
        Returns the focused item.
        """
        for child in self.list_frame.winfo_children():
            if child.focused:
                return child
        return None

    def change_price_config(self, item, new_price):
        """
        Changes the price configuration.
        """
        current_toggle = self.shopping_manager.left_grid.navbar.current_toggle
        self.shopping_manager.gui.app.config.change_price(current_toggle, item.name, new_price)
        self.loggers.log.debug("Price of item %s has been changed to %s.",
                               item.name, new_price)

    def reset(self):
        """
        Resets the price.
        """
        config_manager = self.manager.manager.gui.app.config
        config_manager.loaded_config = config_manager.load(
            self.manager.manager.gui.app.config.name)
        self.display_item_list()
