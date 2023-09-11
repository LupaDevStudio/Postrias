"""
Module to create images with text on it.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.image import Image
from kivy.properties import (
    StringProperty
)

#############
### Class ###
#############


class ImageWithText(Image):
    """
    Image class with a text label on it.
    """

    # Add new attributes to manage the text
    text = StringProperty()
    font = StringProperty("Roboto")
    text_color = (0, 0, 0, 1)
    text_filling_ratio = 0.9
    text_halign = "center"
    text_valign = "center"
    text_font_size = 15
