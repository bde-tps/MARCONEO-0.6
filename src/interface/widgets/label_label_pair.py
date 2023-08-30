"""
label_label_pair.py

Contains the LabelLabelPair widget
which is a Label and an Entry.
"""

#-------------------------------------------------------------------#

from src.utils.gui_utils import Frame, Label

#-------------------------------------------------------------------#

class LabelLabelPair(Frame):
    """
    Templates containing two labels.
    """
    def __init__(self, master=None, name:str="",
                 price:str="", color:str="",  **kwargs) -> None:
        Frame.__init__(self, master, **kwargs)
        self.configure(bg=color, highlightthickness=3,
                       highlightbackground=self.darken(color))
        self.name = name
        self.color = color
        self.price = price
        self.focused = False
        self.label = Label(self, text=self.name+":", bg=color, font=("system", 12),
                           fg=self.darken(color))
        self.entry = Label(self, text=self.price, bg=color, font=("system", 12),
                           fg=self.darken(color))
        self.label.pack(side='left', padx=10, pady=5)
        self.entry.pack(side='left', padx=10, pady=5)

        # Bindings to cover the whole widget
        self.bind("<Button-1>", self.on_label_click)
        self.label.bind("<Button-1>", self.on_label_click)
        self.entry.bind("<Button-1>", self.on_label_click)

    def on_label_click(self, _event):
        """
        Prints the text of the label.
        """
        for widget in self.master.winfo_children():
            widget.focused = False
            widget.configure(highlightbackground=self.darken(widget.color))

        self.focused = True
        self.config(highlightbackground="#dedede")

    def darken(self, color: str) -> str:
        """
        Darkens the color.
        """
        factor = 0.5
        red, green, blue = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        red_darkened = int(red * factor)
        green_darkened = int(green * factor)
        blue_darkened = int(blue * factor)
        return f"#{format(red_darkened, '02x')}{format(green_darkened, '02x')}{format(blue_darkened, '02x')}"
