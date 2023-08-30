"""
button_app.py

Configure MarcoNeo's app button.
"""

#-------------------------------------------------------------------#

from tkinter import Button

#-------------------------------------------------------------------#

class AppButton(Button):
    """
    Custom button for MarcoNeo's app.
    """
    DEFAULT_BG = "#66b3ff"
    ACTIVE_TOGGLE = "#2683ff"
    def __init__(self, master=None, **kwargs) -> None:
        Button.__init__(self, master, **kwargs)
        self.configure(font=("System", 12), bg=self.DEFAULT_BG,
                            fg="white", activebackground=self.ACTIVE_TOGGLE,
                            activeforeground="#FFFFFF", bd=0, highlightthickness=3,
                            highlightbackground=self.ACTIVE_TOGGLE,
                            relief="flat", padx=10, pady=10, disabledforeground="#FFFFFF",)

class ImageButton(Button):
    """
    Custom button for MarcoNeo's app.
    """
    def __init__(self, master=None, **kwargs) -> None:
        Button.__init__(self, master, **kwargs)
        self.configure( bg="#000000", activebackground="#000000",
                        activeforeground="#000000", bd=0,
                        highlightthickness=0)
