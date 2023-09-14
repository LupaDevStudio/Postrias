"""
Module to create images with text on it and a transparent button.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.button import Button
from kivy.properties import (
    StringProperty,
    ObjectProperty
)

#############
### Class ###
#############


class ImageWithTextButton(Button):
    """
    Image class with a text label on it and a transparent button.
    """

    # Add new attributes to manage the text
    image_source = StringProperty()
    image_size_hint = ObjectProperty((1, 1))
    image_pos_hint = ObjectProperty({"x":0, "y": 0})
    label_text = StringProperty()
    label_font_name = StringProperty("Roboto")
    label_text_color = ObjectProperty([0, 1, 0, 1])
    text_filling_ratio = 0.9
    text_halign = "center"
    text_valign = "center"
    text_font_size = 15
