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

from path import (
    PATH_USER_DATA,
    PATH_MUSICS,
    PATH_SOUNDS
)
from basic_tools import (
    load_json_file,
    save_json_file
)
from game_tools import (
    load_sounds,
    DynamicMusicMixer
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
USER_DATA = load_json_file(PATH_USER_DATA)

### Language ###

DICT_LANGUAGE_CORRESPONDANCE = {
    "french": "Français",
    "english": "English"
}


# TEMP, to move inside the app
# Load the dictionnaries
MUSIC_DICT = load_sounds(PATH_MUSICS, USER_DATA["music_volume"])
SOUND_DICT = load_sounds(PATH_SOUNDS, USER_DATA["sound_volume"])

# Create the mixer
music_mixer = DynamicMusicMixer(MUSIC_DICT)
sound_mixer = DynamicMusicMixer(SOUND_DICT)
