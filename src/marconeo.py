"""
marconeo.py

Defines MarcoNeo's app class.
MarcoNeo class encapsulates the whole logic of the application
as well as the connections to the database and the RFID reader.
"""

#-------------------------------------------------------------------#

from src.utils.loggers import Loggers
from src.client.member import Member
from src.client.cart import Cart
from src.server.config import Config
from src.server.db_cursor import DBCursor
from src.server.payment_service import PaymentService
from src.client.rfid import RFID
from src.interface.user_interface import GUI

#-------------------------------------------------------------------#

class MarcoNeo:
    """
    MarcoNeo's app class.
    MarcoNeo class encapsulates the whole logic of the application
    as well as the connections to the database and the RFID reader.
    """

    NAME = "MARCONEO"
    VERSION = "0.6"

    def __init__(self) -> None:
        """
        MarcoNeo's app class's constructor.
        """
        # Setup the loggers
        self.loggers = Loggers(MarcoNeo.NAME)
        self.loggers.log.info("Starting MarcoNeo v%s...", MarcoNeo.VERSION)

        # Setup the client user
        self.current_user = Member(self)
        self.cart = Cart(self.loggers, self.current_user)

        # Setup the database cursor and payment service
        self.config = Config(self)
        self.db_cursor = DBCursor(self)
        self.payment_service = PaymentService(self)

        # Setup the RFID reader and the GUI
        self.rfid = RFID(self)
        self.loggers.log.info("MarcoNeo launched.")

        self.gui = None
        GUI(self)

    def close(self):
        """
        Quits the application.
        """
        # Close the database connection safely
        self.db_cursor.close()
        # Close the rest of the application
        self.gui.close()
        self.loggers.log.info("Closing MARCONEO...")
        self.loggers.close()

    def update_user(self, user_data:dict=None) -> None:
        """
        Updates the current user to a blank user or to the user_data.
        """
        # If main menu is not loaded, return
        if self.gui.shopping_menu is None:
            return

        # Refill security
        if self.gui.shopping_menu.left_grid.navbar.current_toggle == "Rechargement":
            if not self.gui.shopping_menu.refill_bool:
                if user_data is not None:
                    if user_data["admin"]:
                        self.gui.shopping_menu.refill_bool = True
                        self.gui.shopping_menu.refill_security()
                        return

        # Update application's current data
        self.current_user.__init__(self, user_data)
        self.cart.__init__(self.loggers, self.current_user)

        # Update the GUI
        self.gui.shopping_menu.right_grid.header.member_card.update_card(self.current_user)
        self.gui.shopping_menu.right_grid.body.update_body(
            self.gui.shopping_menu.left_grid.navbar.current_toggle)
        self.gui.shopping_menu.right_grid.footer.update_footer()
