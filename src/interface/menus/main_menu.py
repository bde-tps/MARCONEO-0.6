"""
main_menu.py

Configure MarcoNeo's welcome page.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import AppFrame, AppLabel, ImageButton, Label
from src.interface.menus.shopping.shopping_menu import ShoppingMenu

#-------------------------------------------------------------------#

class MainMenu(AppFrame):
    """
    MarcoNeo's main page.

    It is the first page to appear
    when the application is launched.
    """
    def __init__(self, gui=None) -> None:
        super().__init__(gui)
        self.gui = gui
        self.tek=0
        self.title = AppLabel(self, image=self.gui.logo)
        frame = AppFrame(self, highlightbackground="white",
                         highlightthickness=4)
        self.switch_config_btn = ImageButton(frame, image=self.gui.defaultmarco,
                                             borderwidth=0,
                                             highlightthickness=5,
                                             highlightbackground="white",
                                            command=self.switch_config)
        self.lightbulb_frame = AppFrame(self)
        self.lightbulb_frame.place(relx=0.86, rely=0.80, anchor="se")
        self.custom_btn = ImageButton(self, image=self.gui.configuration,
                                command=lambda: self.gui.change_menu(self.gui.settings_menu))
        self.credits_btn = ImageButton(self, image=self.gui.credits,
                                    command=lambda: self.gui.change_menu(self.gui.credits_menu))
        self.history_btn = ImageButton(self, image=self.gui.history,
                                    command=self.history)
        self.load_btn = ImageButton(self, image=self.gui.load,
                                command=self.load_marco)
        self.power_btn = ImageButton(self, image=self.gui.poweroff,
                                command=self.gui.app.close)


        self.title.place(relx=0.5, rely=0.3, anchor="center")

        self.load_btn.place(relx=0.5, rely=0.60, anchor="center")
        self.switch_config_btn.pack(padx=5, pady=5)
        frame.place(relx=0.5, rely=0.88, anchor="center")

        self.power_btn.place(relx=0.03, rely=0.97, anchor="sw")
        self.credits_btn.place(relx=0.15, rely=0.97, anchor="sw")

        self.history_btn.place(relx=0.97, rely=0.97, anchor="se")
        self.custom_btn.place(relx=0.85, rely=0.97, anchor="se")

    def load_marco(self) -> None:
        """
        Changes the menu to the main menu.
        Config are already loaded, so it just
        changes the menu.
        """
        # Security check
        if self.gui.app.config is None:
            self.gui.app.loggers.log.warn("There is no config file loaded.")
            return

        self.gui.app.config.update_loaded_config()
        # Security check for custom config
        if self.gui.app.config.name == self.gui.app.config.CUSTOM:
            # if there is only the refill menu, it means that the user didn't change anything.
            if len(self.gui.app.config.get_custom_categories()) <= 1:
                self.gui.loggers.log.warn("Config needs to be customed before loading it.")
                if self.lightbulb_frame.winfo_children():
                    self.tek+=1
                    if self.tek==10:
                        for widget in self.gui.winfo_children():
                            widget.destroy()
                        label = Label(self.gui,
                              image=self.gui.tek)
                        label.place(relx=0.5, rely=0.5, anchor="center")
                        label.bind("<Button-1>", lambda e: self.gui.app.close())
                    return
                AppLabel(self.lightbulb_frame, image=self.gui.lightbulb).pack(side='left')
                AppLabel(self.lightbulb_frame, image=self.gui.lightbulb).pack(side='left')
                AppLabel(self.lightbulb_frame, image=self.gui.lightbulb).pack(side='left')
                return

        # Fresh new start
        self.gui.app.current_user.logout()
        self.gui.shopping_menu = ShoppingMenu(self.gui)
        self.gui.change_menu(self.gui.shopping_menu)

    def switch_config(self) -> None:
        """
        Changes the menu to the main menu.
        """
        custom = self.gui.app.config.CUSTOM
        default = self.gui.app.config.DEFAULT
        if self.gui.app.config.name == custom:
            self.gui.app.config.name = default
            self.switch_config_btn.config(image=self.gui.defaultmarco)
        elif self.gui.app.config.name == default:
            self.gui.app.config.name = custom
            self.switch_config_btn.config(image=self.gui.custommarco)
        self.gui.loggers.log.info("Config switched to " + self.gui.app.config.name)

    def history(self) -> True:
        """
        Change menu to history menu.
        """
        self.gui.history_menu.refresh_history()
        self.gui.change_menu(self.gui.history_menu)
        return True
