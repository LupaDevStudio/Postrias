"""
Module for the tutorial menu.
"""

###############
### Imports ###
###############

from tools.path import (
    PATH_IMAGES,
    PATH_TEXT_FONT
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

class TutorialScreen(ImprovedScreen):

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "tutorial_background.jpg",
            font_name=PATH_TEXT_FONT,
            **kw)

    counter_tutorial = 0

    def on_enter(self, *args):
        self.ids.tutorial_text.text = TEXT.tutorial[self.counter_tutorial]
        return super().on_enter(*args)

    def go_to_previous_slide(self):
        """
        Go to the previous slide of the tutorial.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Go to main menu at the beginning
        if self.counter_tutorial == 0:
            self.manager.current = "menu"
        
        else:
            self.counter_tutorial -= 1
            self.ids.tutorial_text.text = TEXT.tutorial[self.counter_tutorial][0]
            self.ids.tutorial_text.source = TEXT.tutorial[self.counter_tutorial][1]

    def go_to_next_slide(self):
        """
        Go to the next slide of the tutorial.
        It can also end the tutorial, when reached the end.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.counter_tutorial += 1

        # Go to game or main menu at the end
        if self.counter_tutorial == len(TEXT.tutorial):

            # For the first launch of the tutorial, go to the game
            if USER_DATA.tutorial:
                USER_DATA.tutorial = False
                USER_DATA.save_changes()
                self.manager.current = "game"

            else:
                self.manager.current = "menu"
        
        else:
            self.ids.tutorial_text.text = TEXT.tutorial[self.counter_tutorial][0]
            self.ids.tutorial_text.source = TEXT.tutorial[self.counter_tutorial][1]
