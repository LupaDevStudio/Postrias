"""
Module for the main menu
"""


from kivy.clock import Clock
from kivy.properties import (
    BooleanProperty
)

from tools.path import (
    PATH_IMAGES,
    PATH_TITLE_FONT
)
from tools.constants import (
    FPS,
    MOBILE_MODE
)
from tools.kivy_tools import ImprovedScreen
from tools import (
    music_mixer,
    game
)


class MenuScreen(ImprovedScreen):

    mobile_mode = BooleanProperty(MOBILE_MODE)
    # title_font = StringProperty(PATH_TITLE_FONT)

    def __init__(self, **kw):

        super().__init__(
            back_image_path=PATH_IMAGES + "menu_background.png",
            font=PATH_TITLE_FONT,
            **kw)
        self.opacity_state = -1
        self.opacity_rate = 0.03

    def on_enter(self, *args):
        # Launch the title music
        music_mixer.play("cinematic_dramatic", loop=True)

        # Schedule the update for the text opacity effect
        Clock.schedule_interval(self.update, 1 / FPS)

        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        # Stop the title music
        music_mixer.stop()

        # Unschedule the clock update
        Clock.unschedule(self.update, 1 / FPS)

        return super().on_leave(*args)

    def update(self, *args):
        self.ids.start_label.opacity += self.opacity_state * self.opacity_rate
        if self.ids.start_label.opacity < 0 or self.ids.start_label.opacity > 1:
            self.opacity_state = -self.opacity_state
