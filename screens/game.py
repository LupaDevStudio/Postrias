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

    def hide_cards(self, *_):
        """
        Hide all cards on the screen.
        """
        cards_list = ["event",
                      "decision_center",
                      "decision_yes",
                      "decision_no",
                      "decision_guillotine",
                      "decree_center",
                      "decree_left",
                      "decree_right"]

        for card in cards_list:
            self.disable_widget(self.ids[card])

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "day_camp.png",
            font_name=PATH_TEXT_FONT,
            ** kw)

        self.decision_cards = ["decision_center",
                               "decision_yes",
                               "decision_no",
                               "decision_guillotine"]

        self.decree_cards = ["decree_center",
                             "decree_left",
                             "decree_right"]

    def on_pre_enter(self, *args):

        # Load the gameplay json
        game.load_resources()
        game.reset_variables()

        # Hide all cards
        self.hide_cards()

        return super().on_pre_enter(*args)

    def on_enter(self, *args):

        # Start the game music
        music_mixer.play("game_music", loop=True)

        # Launch the start day function
        Clock.schedule_once(self.start_day)

        return super().on_enter(*args)

    def display_card(self, *args):
        if game.phase == "decision":
            self.ids["decision_center"].text = game.text_dict["card"]
            self.ids["decision_no"].text = game.text_dict["left"]
            self.ids["decision_yes"].text = game.text_dict["right"]
            for card in self.decision_cards:
                self.enable_widget(self.ids[card])

    def test(self):
        print("toto")

    def start_day(self, *args):
        game.start_day()
        self.display_card()
