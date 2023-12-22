"""
Module for the main menu.
"""

###############
### Imports ###
###############

### Python imports ###

import webbrowser

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
            back_image_path=PATH_IMAGES + "menu_background_christmas.jpg",
            font_name=PATH_TITLE_FONT,
            **kw)
        self.opacity_state = -1
        self.opacity_rate = 0.03
        self.other_screens_loaded = False

    def on_enter(self, *args):
        # Launch the title music
        if music_mixer.musics["cinematic_dramatic"].state == "stop":
            music_mixer.play("cinematic_dramatic", loop=True)

        # Schedule the update for the text opacity effect
        Clock.schedule_interval(self.update, 1 / FPS)

        # Set the start label text
        self.start_label_text = TEXT.menu["press_to_start"]

        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        # Unschedule the clock update
        Clock.unschedule(self.update, 1 / FPS)

        return super().on_leave(*args)

    def update(self, *args):
        self.ids.start_game.opacity += self.opacity_state * self.opacity_rate
        if self.ids.start_game.opacity < 0 or self.ids.start_game.opacity > 1:
            self.opacity_state = -self.opacity_state

    def start_game(self):
        """
        Start the intermediate menu, to choose between a saved or new game.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.manager.current = "intermediate_menu"

    def open_lupa_website(self):
        webbrowser.open("https://lupadevstudio.com", 2)
