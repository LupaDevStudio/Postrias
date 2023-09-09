"""
Module for the game screen
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.clock import Clock
from kivy.properties import StringProperty

### Module imports ###
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

    # Create factions values for Label
    order_value = StringProperty("0")
    military_value = StringProperty("0")
    civilian_value = StringProperty("0")
    paleo_value = StringProperty("0")

    # Create
    food_value = StringProperty("0")
    weapons_value = StringProperty("0")
    tools_value = StringProperty("0")

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
