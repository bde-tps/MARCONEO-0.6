"""
loggers.py

This scripts contains the Logs class.
"""

#------------------------------------------------------------------------------#

import logging
import os
from datetime import datetime

#------------------------------------------------------------------------------#

class Loggers:
    """
    This class represents the logs of the application.
    """
    def __init__(self, name) -> None:
        """
        Constructor of the Logs class.
        """
        self.log_level = logging.DEBUG # Configure log error level
        self.log_name = name
        # Display format in the log
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.log_date_format = "%Y-%m-%d %I:%M:%S"
        self.log_out_path = os.path.join(os.getcwd(), "data", "logs") # Path of the log file
        self.log_path = os.path.join(self.log_out_path, self.log_name + ".log")
        self.create_root_dir()
        self.create_log_file()

    def create_root_dir(self) -> None:
        """
        Create the root directory of the logs.
        """
        if not os.path.exists(self.log_out_path):
            os.makedirs(self.log_out_path)

    def create_log_file(self) -> bool:
        """
        Create the log file.
        """
        # Delete the latest log file and create a new one to avoid conflict between the .log file
        try:
            os.remove(self.log_path)
        except OSError:
            pass
        self.log = logging.getLogger(self.log_name)
        self.log.setLevel(self.log_level)
        logging.basicConfig(filename=self.log_path, format=self.log_format,
                            datefmt=self.log_date_format, level=self.log_level)
        return True

    def close(self) -> bool:
        """
        Add to the log of the day the log of the passed session.
        """
        # Actualize the log file
        now = datetime.now() # Current date and hour
        day_log_path = os.path.join(self.log_out_path, now.strftime("%d-%m-%Y.log"))

        # Copy each line of the log file in the log of the day
        with open(day_log_path,
                  "a",
                  encoding="UTF-8") as day_log, open(self.log_path,
                                                     "r",
                                                     encoding="UTF-8") as session_log:
            for line in session_log:
                day_log.write(line)

            # Separate each session in the log of the day
            day_log.write("--------------------------------------------------------------\n")
            # Close files
            day_log.close()
            session_log.close()

        return True
