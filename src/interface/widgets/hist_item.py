"""
hist_item.py

Defines the HistoryItem class.
"""

#-------------------------------------------------------------------#

import datetime
from src.utils.gui_utils import AppLabel, AppFrame

#-------------------------------------------------------------------#

class HistoryItem(AppFrame):
    """
    Item in which is displayed an order from the history.
    """
    def __init__(self, manager, item_purchased) -> None:
        super().__init__(manager)
        self.member_name = item_purchased[0]
        self.item_name = item_purchased[1]
        self.price = item_purchased[2]
        self.amount = item_purchased[3]
        self.date = item_purchased[4].strftime("%d/%m/%Y %H:%M")
        self.config(bg="#0b1a35")
        self.setup_label()

    def setup_label(self) -> None:
        """
        Defines the labels used in the history item.
        """
        AppLabel(self, text=f"{self.member_name}",
                 font=('system', 12, "bold"), bg="#0b1a35").pack(expand=True, fill='x',
                     side="left", padx=10)

        color = "white"
        if self.price<0:
            color = "green"
        else:
            color = "red"

        AppLabel(self, text=f"{-self.price}€",
                 font=('system', 12, "bold"), bg="#0b1a35", fg=color).pack(expand=True, fill='x',
                     side="left", padx=10)

        date_lbl = AppLabel(self, text=f"{self.get_day_description(self.date)}",
                 font=('system', 12), bg="#0b1a35")
        date_lbl.pack(side="right", padx=10, expand=True, fill='x')
        date_lbl.configure(anchor="center")

        AppLabel(self, text=f"{self.amount} x {self.item_name}",
                 font=('system', 12), bg="#0b1a35").pack(side="left", padx=10)

    def get_day_description(self, date:datetime.datetime):
        """
        Returns a description of the date given.
        """
        formated_date = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")
        now = datetime.datetime.now().date()
        diff = now - formated_date.date()
        if diff.days == 0:
            return f"Aujourd'hui {formated_date.strftime('%H:%M')}"
        if diff.days == 1:
            return f"Hier {formated_date.strftime('%H:%M')}"
        if diff.days == 2:
            return f"Avant-hier {formated_date.strftime('%H:%M')}"
        return date
