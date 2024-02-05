"""
rfid.py

This file is responsible for the RFID reader.
MarcoNeo app uses the binding tkinter method
to listen to the RFID reader.
"""

#------------------------------------------------------------#
from src.utils.hardware import key_to_number

class RFID:
    """
    Defines the RFID reader.
    """
    def __init__(self, app) -> None:
        """
        Constructor of the RFID class.
        """
        self.app = app
        self.loggers = self.app.loggers
        self.current_user_id = None
        self.buffer = ""

    def rfid_callback(self, event) -> None:
        """
        Callback function for the RFID reader.
        """
        # If the user presses the enter key (or keypad enter key), the buffer is parsed
        if event.keysym in ('Return', 'KP_Enter'):
            if self.buffer == "":
                return  # If the buffer is empty, do nothing

            self.loggers.log.debug(f"Parsing RFID card number {self.buffer}...")
            try:
                id_in_buffer = key_to_number(self.buffer)
            except ValueError:
                self.loggers.log.error("RFID card corrupted.")
                self.buffer = ""  # Reset the buffer
                self.app.update_user(None)
                return
            user = self.app.db_cursor.get_member(id_in_buffer)
            if user is None:
                self.buffer = ""  # Reset the buffer
            self.app.update_user(user)

            self.buffer = ""  # Reset the buffer

        else:
            self.buffer += event.char
