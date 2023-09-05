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
from kivy.config import Config

### Local imports ###
from tools.tools_basis import (
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

### Kivy parameters ###

FPS = 30
MSAA_LEVEL = 2

Config.set("graphics", "maxfps", FPS)
Config.set("graphics", "multisamples", MSAA_LEVEL)

### Paths ###

# Path for the folders
PATH_RESOURCES_FOLDER = "resources/"

# Path for the user data
PATH_USER_DATA = "data.json"

# Path for the resources
PATH_LANGUAGE = PATH_RESOURCES_FOLDER + "languages/"
PATH_IMAGES = PATH_RESOURCES_FOLDER + "images/"
PATH_MAP_TEXTURES = PATH_IMAGES + "map_textures/"
PATH_ATLAS = PATH_RESOURCES_FOLDER + "atlas/"
PATH_KIVY_FOLDER = PATH_RESOURCES_FOLDER + "kivy/"
PATH_MAPS = PATH_RESOURCES_FOLDER + "maps/"
PATH_SOUNDS = PATH_RESOURCES_FOLDER + "sounds/"
PATH_MUSICS = PATH_RESOURCES_FOLDER + "musics/"
PATH_FONTS = PATH_RESOURCES_FOLDER + "fonts/"

# Path for the fonts
PATH_TITLE_FONT = PATH_FONTS + "scratched_letters.ttf"
PATH_TEXT_FONT = PATH_FONTS + "another_typewriter.ttf"

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
