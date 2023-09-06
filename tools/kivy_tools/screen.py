"""
Module to deal with fonts in kivy.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen as KivyScreen
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty,
    BooleanProperty
)

###############
### Classes ###
###############


class ImprovedScreen(KivyScreen):
    """
    Improved Screen class based on the kivy one.
    """

    # Create the back image properties
    back_image_width = NumericProperty(Window.size[0])
    back_image_height = NumericProperty(Window.size[1])
    back_image_disabled = BooleanProperty(False)
    back_image_path = StringProperty()

    def __init__(self, back_image_path=None, **kw):

        # Init the kv screen
        super().__init__(**kw)

        # Set the background image
        if back_image_path is not None:
            self.back_image_opacity = 1
            self.back_image_disabled = False
        else:
            self.back_image_path = ""
            self.back_image_opacity = 0
            self.back_image_disabled = True

    def set_back_image(self, back_image_path):
        """
        Set a background image for the screen.
        """
        self.back_image_path = back_image_path
        self.back_image_ratio = 0

    def update_back_image_size(self):
        self.back_image_width = Window.size[0]
        self.back_image_width = Window.size[0]

    def init_screen(self, *args, **kwargs):
        pass

    @property
    def font_ratio(self):
        """
        Font ratio to use on the screen to keep letter size constant with Window size changes.
        """
        return Window.size[0] / 1600
