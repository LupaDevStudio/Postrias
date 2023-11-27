"""
Module for the main menu.
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
from tools import (
    music_mixer
)

###############
### Classes ###
###############

class MenuScreen(ImprovedScreen):

    start_label_text = StringProperty()

    def __init__(self, **kw):

        super().__init__(
            back_image_path=PATH_IMAGES + "menu_background.jpg",
            font_name=PATH_TITLE_FONT,
            **kw)
        self.opacity_state = -1
        self.opacity_rate = 0.03

    def on_enter(self, *args):
        # Launch the title music
        if music_mixer.musics["cinematic_dramatic"].state == "stop":
            music_mixer.play("cinematic_dramatic", loop=True)

        # Schedule the update for the text opacity effect
        Clock.schedule_interval(self.update, 1 / FPS)

        # Schedule preload of the game screen
        Clock.schedule_once(self.manager.get_screen("game").preload)

        # Set the start label text
        self.start_label_text = TEXT.menu["press_to_start"]

        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        # Stop the title music
        if self.manager.current != "settings":
            music_mixer.stop()

        # Unschedule the clock update
        Clock.unschedule(self.update, 1 / FPS)

        return super().on_leave(*args)

    def update(self, *args):
        self.ids.start_label.opacity += self.opacity_state * self.opacity_rate
        if self.ids.start_label.opacity < 0 or self.ids.start_label.opacity > 1:
            self.opacity_state = -self.opacity_state

    def start_game(self):
        """
        Start the tutorial for the first time, otherwise the game.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if USER_DATA.tutorial:
            self.manager.current = "tutorial"
        else:
            self.manager.current = "game"
