"""
sett_header.py

Header of the settings page of the app.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Frame, ImageButton, AppLabel

#-------------------------------------------------------------------#

class SettHeader(Frame):
    """
    Header of the settings page of the app.
    """
    def __init__(self, manager=None) -> None:
        super().__init__(manager)
        self.manager = manager
        self.config(bg="#000000", highlightbackground= "#4d88ff",
                    highlightthickness=5)
        self.propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        AppLabel(self,
              image=self.manager.manager.gui.customize_lbl).pack(side="left",expand=True)
        AppLabel(self,
              image=self.manager.manager.gui.select_lbl).pack(side="left",expand=True)
        ImageButton(self, image=self.manager.manager.gui.refresh,
                  command=self.manager.manager.refresh).pack(side="right")
        ImageButton(self, image=self.manager.manager.gui.discard,
                    command=self.manager.manager.refresh).pack(side="right")
