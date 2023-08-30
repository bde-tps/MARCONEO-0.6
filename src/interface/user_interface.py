"""
graphic_user_interface.py

This script describes the GUI class.
It is responsible for the GUI of the MarcoNeo application.
"""

#------------------------------------------------------------#

import os
import logging




from src.utils.gui_utils import Tk, Frame, BOTH, Image, ImageTk, ImageOps, ImageFilter
from src.interface.menus.main_menu import MainMenu
from src.interface.menus.credits_menu import CreditsMenu
from src.interface.menus.settings.settings_menu import SettingsMenu
from src.interface.menus.history_menu import HistoryMenu

#------------------------------------------------------------#

logger = logging.getLogger('PIL.PngImagePlugin')
logger.setLevel(logging.WARNING)

#------------------------------------------------------------#

class GUI(Tk):
    """
    Graphical User Interface of the application.
    """
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.loggers = self.app.loggers
        self.protocol("WM_DELETE_WINDOW", self.app.close)
        self.main_menu = None
        self.shopping_menu = None
        self.history_menu = None
        self.stats_menu = None

        self.bind("<Key>", self.app.rfid.rfid_callback) # Listen to the RFID reader
        self.loggers.log.debug("RFID is listening.")

        self.setup_window()
        self.load_images()

        self.shopping_menu = None
        self.main_menu = MainMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.history_menu = HistoryMenu(self)
        self.main_menu.pack(fill=BOTH, expand=True)
        self.current_menu = self.main_menu

        # Set the GUI reference in the application
        setattr(self.app, "gui", self)
        self.mainloop()

    def change_menu(self, next_menu: Frame) -> None:
        """
        This function changes the current view to the desired menu.
        """
        # Don't do anything if the desired menu is the same as the current menu
        if next_menu == self.current_menu:
            return

        # Unbind the keyboard
        self.unbind("<Key>")

        next_menu.pack(fill=BOTH, expand=True)

        # Check night mode

        self.current_menu.pack_forget()

        # Re-bind the keyboard
        self.bind("<Key>", self.app.rfid.rfid_callback)

        # Update the current menu reference
        self.current_menu = next_menu
        self.loggers.log.debug(f"({type(next_menu).__name__})")

    def setup_window(self) -> bool:
        """
        Setup the window of the application.
        """
        self.title("MarcoNeo")
        self.geometry("800x480")
        self.resizable(False, False)
        #self.iconbitmap(os.path.join(os.getcwd(),"DATA","IMAGES","logo.ico"))
        #self.config(bg="black")
        return True

    def start(self) -> bool:
        """
        Displays the GUI.
        """
        self.mainloop()
        return True

    def close(self) -> bool:
        """
        This function is called when the user closes the application.
        """
        self.quit()
        self.loggers.log.debug("GUI closed.")
        return True

    def load_images(self) -> None:
        """
        Load every image of the application.
        """
        # general
        self.back = self.open_image("back.png", 70, 70)
        self.refresh = self.open_image("refresh.png", 70, 70)

        # main_menu
        self.logo = self.open_image("MarcoNeo.png")
        self.poweroff = self.open_image("power.png", 70, 70)
        self.configuration = self.open_image("config.png", 70, 70)
        self.lightbulb = self.open_image("lightbulb.png", 30, 30)
        self.load = self.open_image("load.png", 130, 130)
        self.tek = self.open_image("tek.png", 1000, 480)
        self.configtek = self.open_image("config.png", 300, 300)

        # credits_menu
        self.credits = self.open_image("credits.png", 70, 70)
        self.credits_txt = self.open_image("credits_txt.png", 450, 300)

        # history_menu
        self.history = self.open_image("history.png", 70, 70)
        self.history_lbl = self.open_image("history_lbl.png", 400, 60)

        # shopping_menu
        self.discard = self.open_image("discard.png", 70, 70)
        self.cart = self.open_image("cart.png", 50, 50)
        self.confirm = self.open_image("confirm.png", 70, 70)
        self.crown = self.open_image("crown.png", 70, 70)
        self.pricemodifier = self.open_image("pricemodifier.png", 50, 50)
        self.cancel = self.open_image("cancel.png", 70, 70)
        self.resetprice = self.open_image("resetprice.png", 70, 70)
        self.logout = self.open_image("logout.png", 50, 50)
        self.id = self.open_image("ID.png", 70, 70)
        self.warning = self.open_image("warning.png", 50, 50)
        self.refill_lbl = self.open_image("refill_lbl.png", 550, 160)
        self.recharger_lbl = self.open_image("recharger_lbl.png", 550, 110)

        # labels
        self.confirm_lbl = self.open_image("confirm_lbl.png", 450, 50)
        self.credits_lbl = self.open_image("credits_lbl.png", 260, 60)
        self.noncotisant_lbl = self.open_image("noncotisant.png", 150, 20)
        self.customisemarco = self.open_image("customisemarco.png", 70, 70)
        self.custommarco = self.open_image("custommarco.png", 135, 70)
        self.defaultmarco = self.open_image("defaultmarco.png", 200, 70)
        self.debiter = self.open_image("debiter.png", 500, 100)

        # price modifier
        self.btn1 = self.open_image("1.png", 78, 78)
        self.btn2 = self.open_image("2.png", 78, 78)
        self.btn3 = self.open_image("3.png", 78, 78)
        self.btn4 = self.open_image("4.png", 78, 78)
        self.btn5 = self.open_image("5.png", 78, 78)
        self.btn6 = self.open_image("6.png", 78, 78)
        self.btn7 = self.open_image("7.png", 78, 78)
        self.btn8 = self.open_image("8.png", 78, 78)
        self.btn9 = self.open_image("9.png", 78, 78)
        self.btn0 = self.open_image("0.png", 78, 78)
        self.dot = self.open_image("dot.png", 78, 78)
        self.backspace = self.open_image("backspace.png", 78, 78)
        self.priceconfirm = self.open_image("priceconfirm.png", 3*78+30, 78)

        # customize menu
        self.customize_lbl = self.open_image("customisez.png", 200, 50)
        self.select_lbl = self.open_image("selectionnez.png", 260, 50)


    def open_image(self, file_name: str,
                   width:int=None, height:int=None, color=None) -> ImageTk.PhotoImage:
        """
        This function loads an image from the given path.
        """
        image_path = os.path.join(os.getcwd(), "data", "images", file_name)
        image = Image.open(image_path)
        if width and height:
            image = image.resize((width, height), Image.ANTIALIAS)
        if color:
            image = image.convert('L')
            image = ImageOps.colorize(image, "#000000",
                                      color,).filter(ImageFilter.GaussianBlur(1))
        photo = ImageTk.PhotoImage(image)
        return photo
