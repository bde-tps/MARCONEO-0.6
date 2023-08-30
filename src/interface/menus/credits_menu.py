"""
credits_menu.py

Configure MarcoNeo's credits page.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import AppFrame, AppLabel, ImageButton

#-------------------------------------------------------------------#

class CreditsMenu(AppFrame):
    """
    MarcoNeo's credits page.

    It contains every contributor to the project.
    """
    def __init__(self, gui=None) -> None:
        super().__init__(gui)
        self.gui = gui
        title_frame = AppFrame(self)
        title_frame.place(relx=0.5, rely=0.10, anchor="center")
        self.title = AppLabel(title_frame, image=self.gui.credits_lbl)
        self.credits_img = AppLabel(title_frame, image=self.gui.credits)

        self.credits_label = AppLabel(self, image=self.gui.credits_txt)
        self.back_btn = ImageButton(self, image=self.gui.back,
                                  command=lambda: self.gui.change_menu(self.gui.main_menu))

        self.credits_img.pack(side="left", padx=(0, 10))
        self.title.pack(side="left")
        self.credits_label.place(relx=0.5, rely=0.55, anchor="center")
        self.back_btn.place(relx=0.02, rely=0.01, anchor="nw")
