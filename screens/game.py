"""
Module for the game screen
"""

###############
### Imports ###
###############

### Python imports ###

import sys
from typing import Literal
sys.path.append(".")

### Kivy imports ###

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.loader import Loader, ProxyImage

### Module imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_IMAGES,
    PATH_MUSICS,
    PATH_SOUNDS
)
from tools.constants import (
    NUMBER_ADS_CREDITS
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
    SOUND_LIST,
    TEXT,
    platform,
    REWARD_INTERSTITIAL,
    INTERSTITIAL
)
if platform == "android":
    from kivads import (
        RewardedInterstitial,
        InterstitialAd
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
                             "decree_down",
                             "decree_center_bg"]

        self.event_cards = ["event", "next_button"]

        self.answer_cards = ["answer", "next_button"]

        self.pre_game_over_cards = ["decision_center",
                                    "decision_yes",
                                    "decision_no"]

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

        self.credit: int
        self.help_mode = False

        self.game_mode = "new"

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
                      "minus_tools",
                      "decree_center_bg"]

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
        self.disable_widget("back_button")

        if not self.help_mode:

            # Load the gameplay json
            game.load_resources()
            if self.game_mode == "new":
                game.reset_variables()
                # Hide all cards
                self.hide_cards()
            else:
                self.load_game()
            self.update_display_resources()

    def on_enter(self, *args):

        if not self.help_mode:

            # Start the game music
            music_mixer.play("game_music", loop=True)

            if self.game_mode == "new":
                # Launch the start day function
                Clock.schedule_once(self.start_day)

                # Allocate the number of credits
                self.credit = NUMBER_ADS_CREDITS

                # Load an add
                if platform == "android":
                    self.reward_interstitial = RewardedInterstitial(
                        REWARD_INTERSTITIAL, self.schedule_reward
                    )
                    self.reward_static = InterstitialAd(
                        INTERSTITIAL
                    )

        else:
            self.help_mode = False

        return super().on_enter(*args)

    def display_card(self, *_):
        """
        Load and display the cards depending on the game phase.
        """
        # Increase the counter of days
        self.ids.day_indicator.text = TEXT.game["day"] + str(game.day)
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
        if not game.game_over:
            self.play_choice_sound(choice=choice)
            game.make_choice(choice=choice)
            game.end_day()
            self.display_answer()
            self.disable_widget("back_button")
        else:
            if choice == "right":
                self.play_ads()
            else:
                self.manager.current = "game_over"

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
        if self.help_mode:
            pass
        else:
            if self.is_answer:
                self.is_answer = False
                self.start_day()
            else:
                self.choose_answer("down")

    def start_day(self, *_):
        """
        Start a new day with a new batch of cards.
        """
        self.enable_widget("back_button")

        if not game.game_over:
            # Hide the cards
            self.hide_cards()

            # Initialise the new day
            game.start_day()

            # Display the new cards
            self.display_card()

            # Set the day background
            self.set_back_image_texture(self.day_camp_background.image.texture)

            self.save_game()
        else:
            self.disable_widget("back_button")
            self.update_display_resources()
            if self.credit > 0:
                self.show_pre_game_over()
            else:
                self.manager.current = "game_over"

    def show_pre_game_over(self):
        """
        Display the pre game over screen with choice to die or to watch an add.
        """
        self.hide_cards()
        self.enable_cards(self.pre_game_over_cards)
        self.ids["decision_center"].text = TEXT.game["pre_game_over"]
        self.ids["decision_yes"].text = TEXT.game["watch_ad"]
        self.ids["decision_no"].text = TEXT.game["go_to_game_over"]

    def play_ads(self):
        """
        Play an ad to continue the game.
        """
        if platform == "android":
            self.reward_interstitial.show()
        else:
            Clock.schedule_once(self.get_ads_reward)

    def schedule_reward(self):
        Clock.schedule_once(self.get_ads_reward)

    def get_ads_reward(self, *args):
        """
        Called after the ad to continue the game.
        """
        if platform == "android":
            self.reward_static.show()
        self.credit = self.credit - 1
        game.continue_game()
        self.update_display_resources()
        self.start_day()
        # Load an add
        if platform == "android":
            self.reward_interstitial = RewardedInterstitial(
                REWARD_INTERSTITIAL, self.schedule_reward
            )
            self.reward_static = InterstitialAd(
                INTERSTITIAL
            )

    def display_factions_help(self):
        self.help_mode = True
        self.manager.get_screen("help").help_mode = "factions_help"
        self.manager.current = "help"

    def display_resources_help(self):
        self.help_mode = True
        self.manager.get_screen("help").help_mode = "resources_help"
        self.manager.current = "help"

    def go_to_menu(self):
        self.manager.current = "menu"

    def save_game(self):
        save_dict = {}
        save_dict["card_id"] = game.card_id
        save_dict["phase"] = game.phase
        save_dict["day"] = game.day
        save_dict["food"] = game.food
        save_dict["weapons"] = game.weapons
        save_dict["tools"] = game.tools
        save_dict["military"] = game.military
        save_dict["civilian"] = game.civilian
        save_dict["paleo"] = game.paleo
        save_dict["order"] = game.order
        save_dict["credit"] = self.credit
        USER_DATA.saved_data = save_dict
        USER_DATA.save_changes()

    def load_game(self):
        save_dict = USER_DATA.saved_data
        game.card_id = save_dict["card_id"]
        game.phase = save_dict["phase"]
        game.day = save_dict["day"]
        game.food = save_dict["food"]
        game.weapons = save_dict["weapons"]
        game.tools = save_dict["tools"]
        game.military = save_dict["military"]
        game.civilian = save_dict["civilian"]
        game.paleo = save_dict["paleo"]
        game.order = save_dict["order"]
        self.credit = save_dict["credit"]
        game.extract_texts()
        self.hide_cards()
        self.enable_widget("back_button")
        self.display_card()

    def reset_variables(self):
        game.reset_variables()
        self.start_day()
