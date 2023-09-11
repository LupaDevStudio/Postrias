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
from tools.constants import TEXT
from tools import (
    music_mixer,
    game
)
from tools.kivy_tools import (
    ImprovedScreen
)


#############
### Class ###
#############


class GameScreen(ImprovedScreen):

    # Create factions values for Label
    order_value = StringProperty("0")
    military_value = StringProperty("0")
    civilian_value = StringProperty("0")
    paleo_value = StringProperty("0")

    # Create resources values for Label
    food_value = StringProperty("0")
    weapons_value = StringProperty("0")
    tools_value = StringProperty("0")

    # Create text for decisions
    decision_text = StringProperty()
    decision_no_text = StringProperty()
    decision_yes_text = StringProperty()

    # Create text for events
    event_text = StringProperty()

    # Create text for decrees
    decree_center_text = StringProperty(TEXT.game["decree"])
    decree_right_text = StringProperty()
    decree_left_text = StringProperty()

    font = StringProperty(PATH_TEXT_FONT)

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "day_camp.png",
            font=PATH_TEXT_FONT,
            ** kw)
        self.font = PATH_TEXT_FONT

    def on_pre_enter(self, *args):

        # Load the gameplay json
        game.load_resources()
        game.reset_variables()

        return super().on_pre_enter(*args)

    def on_enter(self, *args):

        # Start the game music
        music_mixer.play("game_music", loop=True)

        Clock.schedule_once(self.start_day)

        return super().on_enter(*args)

    def display_card(self, *args):
        if game.phase == "decision":
            pass

    def start_day(self, *args):
        game.start_day()
        self.display_card()
