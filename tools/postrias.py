"""
Module for the game class of postrias.
"""

###############
### Imports ###
###############

### Python imports ###

import random
from typing import Literal

### Module imports ###

from tools.basic_tools import load_json_file
from tools.path import PATH_GAMEPLAY
from tools.constants import TEXT

#################
### Constants ###
#################

EVENT_PROBABILITY = 0.1
DECREE_DELAY = 7
RESOURCES_START_VALUE = 50
FACTION_START_VALUE = 50
RESOURCES_CONSO_PER_DAY = 3
MALUS_ON_EXECUTION = 10

#############
### Class ###
#############


class Game():
    """
    Class to manage all variables during a game of Postrias.
    """

    def __init__(self) -> None:

        # Reset variables
        self.reset_variables()
        self.reset_effect_dict()

        # Initialise other variables
        self.phase: str
        self.gameplay: dict
        self.card_id: str
        self.ending: str
        self.ending_text: str
        self.score: int
        self.text_dict = {}
        self.game_over = False

    def load_resources(self):
        """
        Load all resources necessary to run the game.
        """
        self.gameplay = load_json_file(PATH_GAMEPLAY)

    def reset_effect_dict(self):
        """
        Reset the dictionnary containing the effects to apply.
        """
        self.effect_dict = {
            "order": 0,
            "military": 0,
            "civilian": 0,
            "paleo": 0,
            "food": 0,
            "tools": 0,
            "weapons": 0
        }

    def reset_variables(self):
        """
        Initialise the game variables to their default values.
        """

        # Day counter
        self.day = 0

        # Resources
        self.food = RESOURCES_START_VALUE
        self.weapons = RESOURCES_START_VALUE
        self.tools = RESOURCES_START_VALUE

        # Factions
        self.military = FACTION_START_VALUE
        self.civilian = FACTION_START_VALUE
        self.order = FACTION_START_VALUE
        self.paleo = FACTION_START_VALUE

    def draw(self, mode: Literal["event", "decree", "decision"]) -> str:
        """
        Draw an id corresponding to the given mode.
        """

        # Extract the ids of the cards
        cards_ids = list(self.gameplay[mode].keys())

        # Pick a random id
        if mode in ("event", "decision"):
            choosen_id = random.randint(0, len(cards_ids) - 1)
            choosen_card_id = cards_ids[choosen_id]
        else:
            choosen_card_id = random.sample(cards_ids, 3)

        return choosen_card_id

    def end_day(self):
        """
        End the current day in the game.

        Apply all the effects contained in the dict and check the game over
        conditions.
        """

        # Apply the effects
        self.food += self.effect_dict["food"]
        self.tools += self.effect_dict["tools"]
        self.weapons += self.effect_dict["weapons"]
        self.order += self.effect_dict["order"]
        self.military += self.effect_dict["military"]
        self.civilian += self.effect_dict["civilian"]
        self.paleo += self.effect_dict["paleo"]

        # Check the game over conditions for resources
        self.game_over = True
        if self.food <= 0:
            self.ending = "food"
        elif self.tools <= 0:
            self.ending = "tools"
        elif self.weapons <= 0:
            self.ending = "weapons"
        elif self.order <= 0:
            self.ending = "order_min"
        elif self.order >= 100:
            self.ending = "order_max"
        elif self.military <= 0:
            self.ending = "military_min"
        elif self.military >= 100:
            self.ending = "military_max"
        elif self.civilian <= 0:
            self.ending = "civilian_min"
        elif self.civilian >= 100:
            self.ending = "civilian_max"
        elif self.paleo <= 0:
            self.ending = "paleo_min"
        elif self.paleo >= 100:
            self.ending = "paleo_max"
        else:
            self.game_over = False

        # Load the ending text
        if self.game_over:
            self.ending_text = TEXT.ending[self.ending]["text"]
            self.score = self.compute_score()

    def compute_score(self):
        """
        Compute the score at the end of the game.
        """
        score = self.day * 100
        score += self.food * 15
        score += self.tools * 15
        score += self.weapons * 15
        score += 50 - abs(self.paleo - 50) * 2
        score += 50 - abs(self.military - 50) * 2
        score += 50 - abs(self.order - 50) * 2
        score += 50 - abs(self.civilian - 50) * 2
        return score

    def start_day(self):
        """
        Start a new day in the game.

        It determines which phase has to be played and draws the card for it.
        """

        # Raise an error if the gameplay json is not loaded
        if self.gameplay is None:
            raise ValueError("The game has not been initialised.")

        # Reset the effect dictionnary
        self.reset_effect_dict()

        # Increment the day counter
        self.day += 1

        # Decrease resources
        self.effect_dict["food"] -= RESOURCES_CONSO_PER_DAY
        self.effect_dict["tools"] -= RESOURCES_CONSO_PER_DAY
        self.effect_dict["weapons"] -= RESOURCES_CONSO_PER_DAY

        # Determine which phase has to be played
        if self.day % DECREE_DELAY == 0:
            self.phase = "decree"
        elif random.random() < EVENT_PROBABILITY:
            self.phase = "event"
        else:
            self.phase = "decision"

        # Draw the card corresponding to the phase
        self.card_id = self.draw(self.phase)

        # Extract the texts to display
        if self.phase == "decree":
            self.text_dict["card"] = TEXT.game["decree"]
            self.text_dict["left"] = TEXT.decree[self.card_id[0]]["text"]
            self.text_dict["down"] = TEXT.decree[self.card_id[1]]["text"]
            self.text_dict["right"] = TEXT.decree[self.card_id[2]]["text"]
        elif self.phase == "event":
            self.text_dict["card"] = TEXT.event[self.card_id]["text"]
        elif self.phase == "decision":
            self.text_dict["card"] = TEXT.decision[self.card_id]["text"]
            self.text_dict["left"] = TEXT.decision[self.card_id]["no"]
            self.text_dict["right"] = TEXT.decision[self.card_id]["yes"]
        else:
            raise ValueError

    def add_effect(self, consequence_dict: dict):
        """
        Add the effects of a choice to the effect dict.
        """

        for key in consequence_dict:
            self.effect_dict[key] += consequence_dict[key]

    def continue_game(self):
        if abs(self.order - 50) >= 50:
            self.order = 50
        if abs(self.military - 50) >= 50:
            self.military = 50
        if abs(self.civilian - 50) >= 50:
            self.civilian = 50
        if abs(self.paleo - 50) >= 50:
            self.paleo = 50
        if self.food <= 0:
            self.food = 30
        if self.tools <= 0:
            self.tools = 30
        if self.weapons <= 0:
            self.weapons = 30
        self.game_over = False

    def make_choice(self, choice: Literal["left", "down", "right"]):
        """
        Treat the decision of the player.
        """

        if self.phase == "decree":

            # Select the decree using the given direction
            if choice == "left":
                idx = 0
            elif choice == "down":
                idx = 1
            elif choice == "right":
                idx = 2

            # Extract the consequence dict
            consequence_dict = self.gameplay["decree"][self.card_id[idx]]

        elif self.phase == "event":
            # Extract the consequence dict
            consequence_dict = self.gameplay["event"][self.card_id]

        elif self.phase == "decision":
            # Interpret the direction
            if choice == "left":
                choice = "no"
            elif choice == "down":
                choice = "guillotine"
            elif choice == "right":
                choice = "yes"

            # Treat the choice to obtain the consequence dict
            if choice in ("yes", "no"):
                consequence_dict = self.gameplay["decision"][self.card_id][choice]
            else:
                consequence_dict = {
                    self.gameplay["decision"][self.card_id]["complainant"]: -
                    MALUS_ON_EXECUTION
                }
        else:
            raise ValueError

        # Add the effect of the decision
        self.add_effect(consequence_dict)

        # Extract the text to display after the choice
        if self.phase in ("decree", "event"):
            self.text_dict["answer"] = TEXT.answer[self.phase]
        elif self.phase == "decision":
            if choice in ["yes", "no"]:
                self.text_dict["answer"] = \
                    TEXT.answer[choice][self.gameplay["decision"]
                                        [self.card_id]["complainant"]]
            else:
                self.text_dict["answer"] = TEXT.answer[choice]


game = Game()
