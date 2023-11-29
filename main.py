"""
Main module of the generator of dialogs.
"""

print("Start Postrias")


###############
### Imports ###
###############


### Python imports ###

import os
import platform
os_name = platform.system()
if os_name == "Windows":
    os.environ['KIVY_TEXT'] = 'pil'
print("Python packages loaded")

### Kivy imports ###

# Disable back arrow
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
print("Kivy packages loaded")

### Module imports ###

from tools.path import (
    PATH_IMAGES,
    PATH_RESOURCES_FOLDER
)
from tools.constants import (
    MOBILE_MODE,
    FPS,
    MSAA_LEVEL
)
from screens import OpeningScreen

print("Local packages loaded")


###############
### General ###
###############


class WindowManager(ScreenManager):
    """
    Screen manager, which allows the navigation between the different menus.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.list_former_screens = []
        opening_screen = OpeningScreen(name="opening")
        self.add_widget(opening_screen)
        self.current = "opening"
        print("WindowManager initialised")


class MainApp(App, Widget):
    """
    Main class of the application.
    """

    def build_config(self, config):
        """
        Build the config file for the application.

        It sets the FPS number and the antialiasing level.
        """
        config.setdefaults('graphics', {
            'maxfps': str(FPS),
            'multisamples': str(MSAA_LEVEL)
        })

    def build(self):
        """
        Build the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        Window.clearcolor = (0, 0, 0, 1)
        self.icon = PATH_IMAGES + "logo.png"

    def on_start(self):
        if MOBILE_MODE:
            Window.update_viewport()

        # Open the menu screen
        # self.root_window.children[0].current = "menu"

        print("Main app started")

        return super().on_start()


# Run the application
if __name__ == "__main__":
    MainApp().run()
