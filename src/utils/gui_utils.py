"""
gui_utils.py

Defines the tkinter classes that are used in the application.
Helps to reduce the number of imports in the other files.
"""

#-------------------------------------------------------------------#

from tkinter import Tk, Frame, Label, Entry, BOTH
from PIL import Image, ImageTk, ImageOps, ImageFilter
from src.interface.widgets.app_button import AppButton, ImageButton
from src.interface.widgets.app_frame import AppFrame
from src.interface.widgets.app_label import AppLabel
from src.interface.widgets.label_label_pair import LabelLabelPair

#-------------------------------------------------------------------#

__all__ = ['Tk', 'Frame', 'Label', 'AppButton',
           'Entry', 'BOTH', 'AppFrame', 'AppButton',
           'LabelLabelPair', 'Image', 'ImageTk', "AppLabel",
           "ImageButton", "ImageOps", "ImageFilter"]
