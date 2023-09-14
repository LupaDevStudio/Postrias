"""
Module to create an improved kivy screen with background and font support.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
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


class ImprovedScreen(Screen):
    """
    Improved Screen class based on the kivy one.
    """

    # Create the back image properties
    back_image_width = NumericProperty(Window.size[0])
    back_image_height = NumericProperty(Window.size[1])
    back_image_disabled = BooleanProperty(False)
    back_image_path = StringProperty()

    # Create the font_name properties
    font_ratio = NumericProperty(1)
    font_name = StringProperty("Roboto")

    def __init__(self, font_name=None, back_image_path=None, **kw):

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
        if font_name is not None:
            self.font_name = font_name

    def set_back_image(self, back_image_path):
        """
        Set a background image for the screen.
        """

        # Set the source of the background image
        self.back_image_path = back_image_path

        # Compute the ratio to use for size computations
        width, height = get_image_size(back_image_path)
        self.back_image_ratio = width / height

        # Update the size of the background image
        self.update_back_image_size()

    def update_back_image_size(self):
        """
        Update the size of the background image
        """
        window_ratio = Window.size[0] / Window.size[1]
        if window_ratio > self.back_image_ratio:
            self.back_image_width = Window.size[0]
            self.back_image_height = Window.size[0] / self.back_image_ratio
        else:
            self.back_image_width = Window.size[1] * self.back_image_ratio
            self.back_image_height = Window.size[1]

    def on_enter(self, *args):
        """
        Initialize the screen when it is opened.
        """

        # Bind to update attributes when the size of the window is changed
        Window.bind(on_resize=self.on_resize)

        # Add the screen name to the list of former screens
        self.manager.list_former_screens.append(self.name)

        # Update the back image size
        self.update_back_image_size()

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
        Update the font_name ratio to use on the screen to keep letter size constant with Window size changes.
        """
        self.font_ratio = Window.size[1] / 600

    def disable_widget(self, widget: Widget):
        """
        Disable the given widget.
        """
        widget.opacity = 0
        widget.disabled = True

    def enable_widget(self, widget: Widget):
        """
        Enable the given widget.
        """
        widget.opacity = 1
        widget.disabled = False
