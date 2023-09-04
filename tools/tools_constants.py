"""
Module referencing the main constants of the application.

Constants
---------
__version__ : str
    Version of the application.

MOBILE_MODE : bool
    Whether the application is launched on mobile or not.

APPLICATION_NAME : str
    Name of the application.

PATH_DATA_FOLDER : str
    Path to the data folder.

PATH_SETTINGS : str
    Path to the json file of settings.

PATH_RESOURCES_FOLDER : str
    Path to the resources folder.

PATH_LANGUAGE : str
    Path to the folder where are stored the json files of language.

PATH_APP_IMAGES : str
    Path to the folder where are stored the images for the application.

PATH_KIVY_FOLDER : str
    Path to the folder where are stored the different kv files.

DICT_LANGUAGE_FONT : dict
    Dictionary associating the code of language to the font.

DICT_LANGUAGE_CORRESPONDANCE : dict
    Dictionary associating the language to its code.
"""


###############
### Imports ###
###############


### Kivy imports ###

from kivy import platform
from kivy.config import Config


from tools.tools_basis import (
    load_json_file
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
OPACITY_RATE = 0.02
MSAA_LEVEL = 4

Config.set("graphics", "maxfps", FPS)
Config.set("graphics", "multisamples", MSAA_LEVEL)

### Paths ###

PATH_DATA_FOLDER = "data/"
PATH_SETTINGS = PATH_DATA_FOLDER + "settings.json"

PATH_RESOURCES_FOLDER = "resources/"
PATH_LANGUAGE = PATH_RESOURCES_FOLDER + "languages/"
PATH_IMAGES = PATH_RESOURCES_FOLDER + "images/"
PATH_MAP_TEXTURES = PATH_IMAGES + "map_textures/"
PATH_ATLAS = PATH_RESOURCES_FOLDER + "atlas/"
PATH_KIVY_FOLDER = PATH_RESOURCES_FOLDER + "kivy/"
PATH_MAPS = PATH_RESOURCES_FOLDER + "maps/"
PATH_CHARACTER_IMAGES = PATH_IMAGES + "ghost_textures/"
PATH_LOGO = PATH_RESOURCES_FOLDER + "start_logo/"
PATH_SOUNDS = PATH_RESOURCES_FOLDER + "sounds/"
PATH_MUSICS = PATH_RESOURCES_FOLDER + "musics/"
PATH_FONTS = PATH_RESOURCES_FOLDER + "fonts/"
PATH_TITLE_FONT = PATH_FONTS + "enchanted_land/Enchanted Land.otf"
SETTINGS = load_json_file(PATH_SETTINGS)

### Language ###

DICT_LANGUAGE_FONT = {
    "french": "Roboto",
    "english": "Roboto"
}

DICT_LANGUAGE_CORRESPONDANCE = {
    "french": "Français",
    "english": "English"
}


#############
### Sound ###
#############


SOUND_VOLUME = 0.5
MUSIC_VOLUME = 0.5

SOUND_RADIUS_CRYSTAL = 3
SOUND_RADIUS_BEACON = 3
PROBABILITY_WATER_DROPS = 0.005

GAME_OVER_FREEZE_TIME = 2
