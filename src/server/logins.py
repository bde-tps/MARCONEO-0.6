"""
logins.py

This module contains the Logins class.
Contains the logins to connect to the database.
"""

#------------------------------------------------------------------------------#

from dataclasses import dataclass

import os

from dotenv import load_dotenv

#------------------------------------------------------------------------------#

@dataclass
class Logins:
    """
    Logins class.
    Contains the logins to connect to the database.
    """
    _host: str = "host"
    _database: str = "marconeo"
    _user: str = "root"
    _password: str = "password"
    _port: int = 3306

    def __init__(self) -> None:
        """
        Logins constructor.
        """
        load_dotenv()

        self._host = os.getenv("DB_BDE_HOST")
        self._database = os.getenv("DB_BDE_DATABASE")
        self._user = os.getenv("DB_BDE_USER")
        self._password = os.getenv("DB_BDE_PASSWORD")
        self._port = os.getenv("DB_BDE_PORT")

    def get_host(self) -> str:
        """
        Returns the host.
        """
        return self._host

    def get_database(self) -> str:
        """
        Returns the database.
        """
        return self._database

    def get_user(self) -> str:
        """
        Returns the user.
        """
        return self._user

    def get_password(self) -> str:
        """
        Returns the password.
        """
        return self._password

    def get_port(self) -> int:
        """
        Returns the port.
        """
        return self._port
