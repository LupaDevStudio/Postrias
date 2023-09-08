"""
Main module of the generator of dialogs.
"""


###############
### Imports ###
###############


### Kivy imports ###

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.widget import Widget

### Module imports ###
from tools.path import (
    PATH_IMAGES
)
from tools.constants import (
    MOBILE_MODE,
    FPS,
    MSAA_LEVEL
)
from tools.kivy_tools.tools_kivy import (
    color_label,
    background_color,
    Window
)
from screens import (   # pylint: disable=unused-import
    MenuScreen,
    GameScreen,
    SettingsScreen,
    GameOverScreen,
    AchievementsScreen
)


# Set the fullscreen
if not MOBILE_MODE:
    # Window.fullscreen = "auto"
    pass


###############
### General ###
###############


class WindowManager(ScreenManager):
    """
    Screen manager, which allows the navigation between the different menus.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gray_color = background_color
        self.color_label = color_label
        self.transition = NoTransition()
        self.add_widget(Screen(name="opening"))
        self.current = "opening"
        self.list_former_screens = []


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
        self.root_window.children[0].current = "menu"

        return super().on_start()


# Run the application
if __name__ == "__main__":
    MainApp().run()
