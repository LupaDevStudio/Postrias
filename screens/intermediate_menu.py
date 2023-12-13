"""
Module for the intermediate menu.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.clock import Clock
from kivy.properties import (
    StringProperty
)

### Module imports ###

from tools.path import (
    PATH_IMAGES,
    PATH_TITLE_FONT
)
from tools.constants import (
    FPS,
    USER_DATA,
    TEXT
)
from tools.kivy_tools import (
    ImprovedScreen
)

###############
### Classes ###
###############


class IntermediateMenuScreen(ImprovedScreen):

    start_label_text = StringProperty()
    continue_label_text = StringProperty()

    def __init__(self, **kw):

        super().__init__(
            back_image_path=PATH_IMAGES + "menu_background.jpg",
            font_name=PATH_TITLE_FONT,
            **kw)
        self.other_screens_loaded = False

    def on_enter(self, *args):

        # Set the labels text
        self.start_label_text = TEXT.menu["new_game"]
        self.continue_label_text = TEXT.menu["continue_game"]

        return super().on_enter(*args)

    def go_to_menu(self):
        """
        Go back to the main menu.
        """

        self.manager.current = "menu"

    def start_game(self, mode):
        """
        Start the tutorial for the first time, otherwise the game.

        Parameters
        ----------
        mode : Literal["new", "continue"]
            Type of game, whether it is a new or a saved game.

        Returns
        -------
        None
        """
        # PAUL
        print(mode)
        if USER_DATA.tutorial:
            self.manager.current = "tutorial"
        else:
            self.manager.current = "game"
