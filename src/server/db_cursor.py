"""
dbcursor.py

Defines the DBCursor class and everything
related to the connexion to the database.
"""

#-------------------------------------------------------------------#

import decimal
import mysql.connector as mysql

from src.utils.decorators import close_service, setup_service, logging_request
from src.client.member import Member
from src.server.logins import Logins

#-------------------------------------------------------------------#

class DBCursor:
    """
    Defines the objects of type cursors that point on the MySQL database.
    It will be able to return information or modify values in the database.
    """
    def __init__(self, app) -> None:
        """
        DataBase's constructor.
        """
        self.loggers = app.loggers
        self.connection = None
        self.cursor = None
        self._logins = Logins()
        self.connect_to_db()
        self.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

    @logging_request
    @setup_service(max_attempts=5)
    def connect_to_db(self) -> bool:
        """
        Connects to the database.
        """
        self.connection = mysql.connect(host=self._logins.get_host(),
                                        database=self._logins.get_database(),
                                        user=self._logins.get_user(),
                                        password=self._logins.get_password(),
                                        port=self._logins.get_port())
        self.cursor = self.connection.cursor()
        self.loggers.log.info("Connected to the database.")
        return True

    @close_service
    def close(self) -> bool:
        """
        Ferme la session MySQL.
        """
        self.connection.close()
        self.loggers.log.debug("Disconnected from the database.")
        return True

    @logging_request
    def get_member(self, card_id:int) -> Member:
        """
        Retrieves a user with the given ID from the database.
        Returns the user if a match is foundin the database, None otherwise
        """
        if card_id < 0:
            return None


        self.cursor.execute("""SELECT id, first_name, last_name, card_number,\
                            balance, admin, contributor
                                FROM members
                                WHERE card_number = %s""", (card_id,))

        result = self.cursor.fetchone()

        if result is not None:
            member_data = {'id':result[0],
                            'first_name':result[1],
                            'last_name':result[2],
                            'card_number':result[3],
                            'balance':result[4],
                            'admin':result[5],
                            'contributor':result[6]}
            self.loggers.log.debug(f"Retrieving member {member_data['first_name']} (ID:{card_id})")
            return member_data
        self.loggers.log.warn(f"No member found with card ID {card_id}")

    @logging_request
    def update_balance(self, member:Member) -> None:
        """
        Updates the balance of the given member in the database.
        """
        if member is None:
            return

        self.cursor.execute("""UPDATE members
                            SET balance = %s
                            WHERE id = %s""", (member.balance, member.member_id))
        self.connection.commit()

        self.loggers.log.debug(f"Member {member.first_name} (ID:{member.card_id}) Balance: {member.balance}")

    @logging_request
    def send_order(self, product_id:int=None, member_id:int=None,
                     price:decimal.Decimal=None, amount:int=None) -> None:
        """
        Sends a command to the database.
        """
        self.cursor.execute("""INSERT INTO orders (product_id, member_id, price, amount)
                               VALUES (%s, %s, %s, %s)
                            """, (product_id, member_id, price*amount, amount))
        self.connection.commit()

    @logging_request
    def get_history(self) -> list:
        """
        Retrieves the history of the given member, including member and product names.
        """
        self.cursor.execute("""SELECT members.first_name AS member_first_name,
                                CASE WHEN products.name IS NULL AND orders.price < 0 THEN 'Rechargement'
                                    ELSE products.name END AS product_name,
                                orders.price,
                                orders.amount,
                                orders.date
                                FROM orders
                                INNER JOIN members ON orders.member_id = members.id
                                LEFT JOIN products ON orders.product_id = products.id
                                WHERE orders.price >= 0 AND orders.product_id IS NOT NULL
                                UNION
                                SELECT members.first_name AS member_first_name,
                                'rechargement' AS product_name,
                                orders.price,
                                orders.amount,
                                orders.date
                                FROM orders
                                INNER JOIN members ON orders.member_id = members.id
                                WHERE orders.price < 0 AND orders.product_id IS NULL
                                ORDER BY date DESC
                                LIMIT 10;
                            """)
        return self.cursor.fetchall()

