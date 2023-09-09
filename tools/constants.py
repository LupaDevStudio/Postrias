"""
Module referencing the main constants of the application.

Constants
---------
__version__ : str
    Version of the application.

MOBILE_MODE : bool
    Whether the application is launched on mobile or not.

PATH_RESOURCES_FOLDER : str
    Path to the resources folder.

PATH_LANGUAGE : str
    Path to the folder where are stored the json files of language.

PATH_APP_IMAGES : str
    Path to the folder where are stored the images for the application.

PATH_KIVY_FOLDER : str
    Path to the folder where are stored the different kv files.

DICT_LANGUAGE_CORRESPONDANCE : dict
    Dictionary associating the language to its code.
"""


###############
### Imports ###
###############

### Python imports ###

import os

### Kivy imports ###

from kivy import platform

### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_LANGUAGE
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)


#################
### Constants ###
#################


### Version ###

__version__ = "2.0.0"

### Mode ###

MOBILE_MODE = platform == "android"
DEBUG_MODE = False
FPS = 30
MSAA_LEVEL = 2


### File loading ###

# Create the user data json if it does not exist
if not os.path.exists(PATH_USER_DATA):
    default_user_data = {
        "language": "english",
        "highscore": 0,
        "endings": {},
        "music_volume": 0.5,
        "sound_effects_volume": 0.5
    }
    save_json_file(PATH_USER_DATA, default_user_data)

# Load the settings


class UserData():
    """A class to store the user data."""

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)
        self.language = data["language"]
        self.highscore = data["highscore"]
        self.endings = data["endings"]
        self.music_volume = data["music_volume"]
        self.sound_effects_volume = data["sound_effects_volume"]


USER_DATA = UserData()

### Language ###


DICT_LANGUAGE_CORRESPONDANCE = {
    "french": "Français",
    "english": "English"
}


class Text():
    def __init__(self, language) -> None:
        self.change_language(language)

    def change_language(self, language):
        """
        Change the language of the text contained in the class.
        """

        # Load the json file
        data = load_json_file(PATH_LANGUAGE + language + ".json")

        # Split the text contained in the screens
        self.menu = data["menu"]
        self.settings = data["settings"]
        self.game_over = data["game_over"]
        self.game = data["game"]

        # Split the text for the cards
        self.decision = data["decision"]
        self.event = data["event"]
        self.ending = data["ending"]
        self.decree = data["decree"]
        self.answer = data["answer"]


TEXT = Text(language=USER_DATA.language)
