"""
Module for the help menu.
"""

###############
### Imports ###
###############

from kivy.properties import StringProperty

from tools.path import (
    PATH_IMAGES,
    PATH_TEXT_FONT,
    PATH_IMAGES_TUTORIAL
)
from tools.kivy_tools import (
    ImprovedScreen
)
from tools.constants import (
    USER_DATA,
    TEXT
)

#############
### Class ###
#############


class HelpScreen(ImprovedScreen):

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "tutorial_background.jpg",
            font_name=PATH_TEXT_FONT,
            **kw)
        self.help_mode = "factions_help"

    def on_pre_enter(self, *args):
        self.ids["help_text"].text = TEXT.game[self.help_mode]
        return super().on_pre_enter(*args)

    def go_back_to_game(self):
        self.manager.current = "game"
