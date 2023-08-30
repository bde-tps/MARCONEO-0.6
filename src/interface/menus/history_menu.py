"""
history_menu.py

Configure MarcoNeo's history page.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import AppLabel, ImageButton, AppFrame, Frame
from src.interface.widgets.hist_item import HistoryItem

#-------------------------------------------------------------------#

class HistoryMenu(AppFrame):
    """
    MarcoNeo's history page.
    """
    MAX_HISTORY = 10
    def __init__(self, gui=None) -> None:
        super().__init__(gui)
        self.gui = gui
        self.setup_headers()
        self.setup_buttons()
        self.history_frame = Frame(self, borderwidth=5, border=5, bg="black",
                                   highlightbackground="#4d88ff", highlightthickness=5)
        self.history_frame.pack(expand=True, fill="both", padx=10, pady=(100, 10))

    def setup_headers(self) -> None:
        """
        Defines the labels used in the history menu.
        """
        frame = AppFrame(self)
        frame.place(relx=0.5, rely=0.10, anchor="center")
        AppLabel(frame, image=self.gui.history).pack(side="left", padx=(0, 10))
        AppLabel(frame, image=self.gui.history_lbl).pack(side="left")

    def setup_buttons(self) -> bool:
        """
        Defines the buttons used in the history menu.
        """
        self.back_btn = ImageButton(self, image=self.gui.back,
                                  command=lambda: self.gui.change_menu(self.gui.main_menu))
        self.refresh_btn = ImageButton(self, image=self.gui.refresh,
                                        command=self.refresh_history)
        self.back_btn.place(relx=0.02, rely=0.01, anchor="nw")
        self.refresh_btn.place(relx=0.98, rely=0.01, anchor="ne")
        return True

    def setup_history(self) -> None:
        """
        Defines the history used in the history menu.
        """
        history = self.gui.app.db_cursor.get_history()
        for item_purchased in history:
            HistoryItem(self.history_frame,
                        item_purchased).pack(expand=True, fill='x', pady=5)
    def refresh_history(self):
        """
        Refesh history on the page
        """
        self.clear_history()
        self.setup_history()
        self.gui.app.loggers.log.info("History have been refreshed.")

    def clear_history(self):
        """
        Clear history on the page
        """
        for widget in self.history_frame.winfo_children():
            widget.destroy()
