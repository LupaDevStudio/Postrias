"""
Module for the game over screen
"""


from kivy.clock import Clock
from tools.path import (
    PATH_TEXT_FONT,
    PATH_IMAGES,
)
from tools.constants import FPS
from tools import (
    music_mixer,
    game
)
from tools.kivy_tools import ImprovedScreen


class GameScreen(ImprovedScreen):
    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "day_camp.png",
            font=PATH_TEXT_FONT,
            ** kw)

    def on_enter(self, *args):

        # Start the game music
        # Temp
        music_mixer.play("game_music", loop=True)

        return super().on_enter(*args)
