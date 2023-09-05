"""
Module to deal with fonts in kivy.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen as KivyScreen

###############
### Classes ###
###############


class Screen(KivyScreen):
    """
    Improved Screen class based on the kivy one.
    """

    def __init__(self, path_back_image, **kw):
        super().__init__(**kw)

    @property
    def font_ratio(self):
        """
        Return the font ratio to use on the screen.
        """
        return Window.size[0] / 1600
