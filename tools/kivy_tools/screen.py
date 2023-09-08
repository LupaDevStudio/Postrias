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
    StringProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.basic_tools import get_image_size

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

    # Create the font properties
    font_ratio = NumericProperty(1)
    font = StringProperty("Roboto")

    def __init__(self, font=None, back_image_path=None, **kw):

        # Init the kv screen
        super().__init__(**kw)

        # Set the background image
        if back_image_path is not None:
            self.set_back_image(back_image_path)
            self.back_image_opacity = 1
            self.back_image_disabled = False
        else:
            self.back_image_path = ""
            self.back_image_opacity = 0
            self.back_image_disabled = True

        # Set the font
        if font is not None:
            self.font = font

    def set_back_image(self, back_image_path):
        """
        Set a background image for the screen.
        """

        # Set the source of the background image
        self.back_image_path = back_image_path

        # Compute the ratio to use for size computations
        width, height = get_image_size(back_image_path)
        self.back_image_ratio = height / width

        # Update the size of the background image
        self.update_back_image_size()

    def update_back_image_size(self):
        """
        Update the size of the background image
        """
        self.back_image_width = Window.size[0]
        self.back_image_height = Window.size[0] * self.back_image_ratio

    def on_enter(self, *args):
        """
        Initialize the screen when it is opened.
        """

        # Bind to update attributes when the size of the window is changed
        Window.bind(on_resize=self.on_resize)

        return super().on_enter(*args)

    def on_leave(self, *args):
        """
        Close when leaving the screen.
        """

        # Unbind the resize update
        Window.unbind(on_resize=self.on_resize)

        return super().on_leave(*args)

    def on_resize(self, *args):
        """
        Update attributes when the window size changes
        """
        self.update_back_image_size()
        self.update_font_ratio()

    def update_font_ratio(self):
        """
        Update the font ratio to use on the screen to keep letter size constant with Window size changes.
        """
        self.font_ratio = Window.size[0] / 800
