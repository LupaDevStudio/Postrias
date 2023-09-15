"""
Module for the game screen
"""

###############
### Imports ###
###############

### Python imports ###

from typing import Literal

### Kivy imports ###

from kivy.clock import Clock
from kivy.properties import StringProperty

### Module imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_IMAGES,
)
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
    """
    Screen used to play the game.
    """

    # Create factions values for Label
    order_value = StringProperty("0")
    military_value = StringProperty("0")
    civilian_value = StringProperty("0")
    paleo_value = StringProperty("0")

    # Create resources values for Label
    food_value = StringProperty("0")
    weapons_value = StringProperty("0")
    tools_value = StringProperty("0")

    # Boolean indicating if the current moment is an answer or not
    is_answer = False

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
                      "decree_right",
                      "decree_down",
                      "answer",
                      "next_button"]

        for card in cards_list:
            self.disable_widget(card)

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
                             "decree_right",
                             "decree_down"]

        self.event_cards = ["event", "next_button"]

        self.answer_cards = ["answer", "next_button"]

    def enable_cards(self, cards_list):
        """
        Enable the given list of cards.
        """
        for card in cards_list:
            self.enable_widget(card)

    def on_pre_enter(self, *args):

        # Load the gameplay json
        game.load_resources()
        game.reset_variables()
        self.update_display_resources()

        # Hide all cards
        self.hide_cards()

        return super().on_pre_enter(*args)

    def on_enter(self, *args):

        # Start the game music
        music_mixer.play("game_music", loop=True)

        # Launch the start day function
        Clock.schedule_once(self.start_day)

        return super().on_enter(*args)

    def display_card(self, *_):
        """
        Load and display the cards depending on the game phase.
        """
        if game.phase == "decision":
            self.ids["decision_center"].text = game.text_dict["card"]
            self.ids["decision_no"].text = game.text_dict["left"]
            self.ids["decision_yes"].text = game.text_dict["right"]
            self.enable_cards(self.decision_cards)
        if game.phase == "decree":
            self.ids["decree_center"].text = game.text_dict["card"]
            self.ids["decree_left"].text = game.text_dict["left"]
            self.ids["decree_right"].text = game.text_dict["right"]
            self.ids["decree_down"].text = game.text_dict["down"]
            self.enable_cards(self.decree_cards)
        if game.phase == "event":
            self.ids["event"].text = game.text_dict["card"]
            self.enable_cards(self.event_cards)

    def choose_answer(self, choice: Literal["left", "right", "down"], *_):
        """
        Treat the action of the player.
        """
        game.make_choice(choice=choice)
        game.end_day()
        self.display_answer()

    def update_display_resources(self):
        """
        Update the values of the seven resources displayed on the screen.
        """
        self.order_value = str(game.order)
        self.military_value = str(game.military)
        self.civilian_value = str(game.civilian)
        self.paleo_value = str(game.paleo)
        self.food_value = str(game.food)
        self.weapons_value = str(game.weapons)
        self.tools_value = str(game.tools)

    def display_answer(self):
        """
        Display the card containing the answer to the previous card.
        It also displays the effects of the decision or the event. TODO
        """
        self.hide_cards()
        self.is_answer = True
        self.update_display_resources()
        # self.display_plus_minus()
        self.enable_cards(self.answer_cards)
        self.ids["answer"].text = game.text_dict["answer"]

    def go_to_next_card(self):
        """
        Go to the next card when clicking on the next button.
        When an answer is currently displayed, we'll go to the next day.
        When an event is displayed, we'll go to the answer to this answer.
        """
        if self.is_answer:
            self.is_answer = False
            self.start_day()
        else:
            self.choose_answer("down")

    def start_day(self, *_):
        """
        Start a new day with a new batch of cards.
        """
        if not game.game_over:
            game.start_day()
            self.hide_cards()
            self.display_card()
        else:
            self.update_display_resources()
            self.manager.current = "game_over"
