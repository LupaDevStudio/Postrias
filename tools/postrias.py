"""
Module for the game class of postrias.
"""

###############
### Imports ###
###############

# Python imports
import random
from typing import Literal

# Module imports
from tools.basic_tools import load_json_file
from tools.path import PATH_GAMEPLAY

#################
### Constants ###
#################

EVENT_PROBABILITY = 0.1
DECREE_DELAY = 7
RESOURCES_START_VALUE = 50
FACTION_START_VALUE = 50

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
        self.has_event: bool
        self.can_decree: bool
        self.event_id: str
        self.decree_id: str
        self.decision_id: str
        self.gameplay: dict

    def load_resources(self):
        """Load all resources necessary to run the game."""
        self.gameplay = load_json_file(PATH_GAMEPLAY)

    def reset_effect_dict(self):
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
        """Initialise the game variables to their default values."""

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

    def draw(self, mode: Literal["events", "decrees", "decisions"]) -> str:
        """Draw a an id corresponding to the given mode."""

        # Extract the ids of the cards
        cards_ids = self.gameplay[mode].keys()

        # Pick a random id
        choosen_id = random.randint(0, len(cards_ids))
        choosen_card_id = cards_ids[choosen_id]

        return choosen_card_id

    def end_day(self):
        pass

    def start_day(self):
        """
        Start a new day in the game.

        It determines which phase have to be played and draws the cards for it.
        """

        # Raise an error if the gameplay json is not loaded
        if self.gameplay is None:
            raise ValueError("The game has not been initialised.")

        # Reset the effect dictionnary
        self.reset_effect_dict()

        # Increment the day counter
        self.day += 1

        # Determine whether to play an event or not
        self.has_event = random.random() < EVENT_PROBABILITY

        # Draw an event if necessary
        if self.has_event:
            self.event_id = self.draw("events")

        # Determine if a decree can be choosen today
        self.can_decree = self.day % DECREE_DELAY == 0

        # Draw a decree if necessary
        if self.can_decree:
            self.decree_id = self.draw("decrees")

        # Draw a decision
        self.decision_id = self.draw("decisions")

    def choose_decree(self, choice):
        pass
