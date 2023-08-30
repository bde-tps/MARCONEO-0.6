"""
MemberCard.py

Member id card displayed on the window.
"""

#------------------------------------------------------------------------------#

from src.utils.gui_utils import Frame, Label

#------------------------------------------------------------------------------#

class MemberCard(Frame):
    """
    Member card displayed on the window.
    """
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.manager =  manager
        self.gui_manager = manager.manager.manager.gui
        self.loggers = self.gui_manager.loggers

        self.configure(bg="#000000")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.noncotisant = Label(self.manager, image=self.gui_manager.noncotisant_lbl,
                  bg="#000000", borderwidth=0)

        self.setup_labels()

    def setup_labels(self) -> bool:
        """
        Defines the labels used in the menu.
        """
        self.name_label = Label(self, text="-",
                                      font=("system", 16, "bold"), fg="#ffffff", bg="#000000")
        self.balance_label = Label(self, text="_", fg="gold",
                                   font=("system", 16, "bold"), bg="#000000")

        self.name_label.pack(padx=5, pady=10)
        self.balance_label.pack(padx=5, pady=(0, 5))

        return True

    def update_card(self, member) -> None:
        """
        Updates the member card with
        the current member's informations.
        """
        if member.card_id is None:
            self.noncotisant.place_forget()
            self.manager.id_card.place_forget()
            self.name_label.configure(text="-")
            self.balance_label.configure(text="_")
            return

        if member.admin:
            self.loggers.log.info("Admin %s connected.", member.first_name)
            self.manager.id_card.configure(image=self.gui_manager.crown)
            self.manager.id_card.place(relx=0.1, rely=0.5, anchor="center")
            self.noncotisant.place_forget()
        elif not member.contributor:
            self.loggers.log.warning("Member %s is not a contributor.", member.first_name)
            self.manager.id_card.configure(image=self.gui_manager.warning)
            self.manager.id_card.place(relx=0.15, rely=0.3, anchor="center")
            self.noncotisant.place(relx=0.15, rely=0.75, anchor="center")
        else:
            self.manager.id_card.configure(image=self.gui_manager.id)
            self.manager.id_card.place(relx=0.1, rely=0.5, anchor="center")
            self.noncotisant.place_forget()

        self.name_label.configure(text=member.first_name + " " + member.last_name)
        self.balance_label.configure(text=f"{member.balance}€")
