"""
Module for the tutorial menu
"""

###############
### Imports ###
###############

from kivy.properties import StringProperty
from tools.path import (
    PATH_IMAGES,
    PATH_TEXT_FONT
)
from tools.kivy_tools import (
    ImprovedScreen
)
from tools.constants import (
    USER_DATA,
    DICT_LANGUAGE_CORRESPONDANCE,
    TEXT
)

#############
### Class ###
#############

class TutorialScreen(ImprovedScreen):

    current_language = StringProperty(
        DICT_LANGUAGE_CORRESPONDANCE[USER_DATA.language])

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "tutorial_background.jpg",
            font_name=PATH_TEXT_FONT,
            **kw)

    counter_tutorial = 0

    def load_labels(self):
        """
        Load the text labels of the screen.
        """
        pass

    def on_enter(self, *args):
        # Load the labels
        self.load_labels()
        return super().on_enter(*args)

    def go_to_previous_slide(self):
        # Go to main menu
        if self.counter_tutorial == 0:
            self.manager.current = "menu"
        
        else:
            self.counter_tutorial -= 1

    def go_to_next_slide(self):
        self.counter_tutorial += 1
        pass
