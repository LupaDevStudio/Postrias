"""
Module for the game screen
"""

###############
### Imports ###
###############

### Python imports ###

from typing import Literal

### Kivy imports ###

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.loader import Loader, ProxyImage

### Module imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_IMAGES,
    PATH_MUSICS,
    PATH_SOUNDS
)
from tools import (
    music_mixer,
    sound_mixer,
    game,
    USER_DATA
)
from tools.kivy_tools import (
    ImprovedScreen
)
from tools.game_tools import (
    load_sounds
)
from tools.constants import (
    MUSIC_LIST,
    SOUND_LIST
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

    # font_size_expand = NumericProperty(1.25)

    # Boolean indicating if the current moment is an answer or not
    is_answer = False

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "day_camp.jpg",
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

        self.plus_minus = ["plus_order",
                           "minus_order",
                           "plus_military",
                           "minus_military",
                           "plus_civilian",
                           "minus_civilian",
                           "plus_paleo",
                           "minus_paleo",
                           "plus_food",
                           "minus_food",
                           "plus_weapons",
                           "minus_weapons",
                           "plus_tools",
                           "minus_tools"]

        self.night_camp_background: ProxyImage
        self.day_camp_background: ProxyImage

    def preload(self, *_):

        if not self.is_loaded:

            # Load the night camp background
            self.night_camp_background = Loader.image(
                PATH_IMAGES + "night_camp.jpg")

            # Load the day camp background
            self.day_camp_background = Loader.image(
                PATH_IMAGES + "day_camp.jpg")

            # Load the musics and sounds
            new_musics = load_sounds(
                MUSIC_LIST, PATH_MUSICS, USER_DATA.music_volume)
            new_sounds = load_sounds(SOUND_LIST, PATH_SOUNDS,
                                     USER_DATA.sound_effects_volume)
            music_mixer.add_sounds(new_musics)
            sound_mixer.add_sounds(new_sounds)

            # Preload the class
            super().preload()

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
                      "next_button",
                      "plus_order",
                      "minus_order",
                      "plus_military",
                      "minus_military",
                      "plus_civilian",
                      "minus_civilian",
                      "plus_paleo",
                      "minus_paleo",
                      "plus_food",
                      "minus_food",
                      "plus_weapons",
                      "minus_weapons",
                      "plus_tools",
                      "minus_tools"]

        for card in cards_list:
            self.disable_widget(card)

    def enable_cards(self, cards_list):
        """
        Enable the given list of cards.
        """
        for card in cards_list:
            self.enable_widget(card)

    def on_pre_enter(self, *args):

        super().on_pre_enter(*args)

        # Load the gameplay json
        game.load_resources()
        game.reset_variables()
        self.update_display_resources()

        # Hide all cards
        self.hide_cards()

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

    def play_choice_sound(self, choice: Literal["left", "right", "down"]):
        """
        Play the sound associated to the choice.
        """

        if game.phase == "decree":
            sound_mixer.play("decree")
        elif game.phase == "decision":
            if choice == "down":
                sound_mixer.play("guillotine")
            else:
                sound_mixer.play("decision")

    def choose_answer(self, choice: Literal["left", "right", "down"], *_):
        """
        Treat the action of the player.
        """
        self.play_choice_sound(choice=choice)
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

    def display_plus_minus(self):
        """
        Display the plus and minus signs.
        """
        for (effect, value) in game.effect_dict.items():
            prefix = None
            if value > 0:
                prefix = "plus"
            elif value < 0:
                prefix = "minus"
            if prefix is not None:
                self.enable_widget(prefix + "_" + effect)

    def display_answer(self):
        """
        Display the card containing the answer to the previous card.
        It also displays the effects of the decision or the event.
        """
        self.set_back_image_texture(self.night_camp_background.image.texture)
        self.hide_cards()
        self.is_answer = True
        self.update_display_resources()
        self.display_plus_minus()
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
            # Hide the cards
            self.hide_cards()

            # Initialise the new day
            game.start_day()

            # Display the new cards
            self.display_card()

            # Set the day background
            self.set_back_image_texture(self.day_camp_background.image.texture)
        else:
            self.update_display_resources()
            self.manager.current = "game_over"

    def rewind(self):
        pass
