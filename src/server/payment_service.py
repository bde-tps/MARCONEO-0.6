"""
payment_service.py

Defines the PaymentService class.
Let the user pay for his purchases.
"""

#-------------------------------------------------------------------#


#-------------------------------------------------------------------#

class PaymentService:
    """
    Defines the PaymentService class.
    """
    def __init__(self, app) -> None:
        self.app = app
        self.current_user = app.current_user
        self.cart = self.app.cart
        self.loggers = app.loggers

    def purchase(self):
        """
        Confirms the purchase.
        """
        if self.current_user.card_id is None:
            self.loggers.log.warning("No user is logged in. Can't purchase.")
            return

        for item in self.cart.items:
            member_id = self.current_user.member_id
            product_id = list(item.keys())[0]
            values = list(item.values())[0]
            price = values[1]
            quantity = values[0]

            # If the product is None, it means the user is adding money to his account.
            # Only products with null id are refillments.
            if product_id is None:
                self.current_user.balance += price*quantity
            else:
                self.current_user.balance -= price*quantity

            self.commit_purchase(product_id=product_id,
                                 member_id=member_id,
                                 price=price,
                                 quantity=quantity)

    def commit_purchase(self, product_id:int=None, member_id:int=None,
                        price:int=None, quantity:int=None) -> None:
        """
        Confirms the purchase.
        """
        self.app.db_cursor.update_balance(self.current_user)
        self.app.db_cursor.send_order(product_id=product_id,
                                        member_id=member_id,
                                        price=price,
                                        amount=quantity)

        self.loggers.log.info("Purchase confirmed. New balance of %s is %s€.",
                              self.current_user.first_name, self.current_user.balance)
        print(f"Purchase confirmed. Your new balance is {self.current_user.balance}€.")
