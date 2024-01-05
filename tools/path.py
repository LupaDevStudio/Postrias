"""
Module to store all the paths used for the app files and folders
"""

##############
### Import ###
##############

import datetime
from kivy.utils import platform


#################
### Constants ###
#################

current_datetime = datetime.datetime.now()
IS_WINTER = current_datetime.month in (1, 2, 12)
MOBILE_MODE = platform == "android"

#############
### Paths ###
#############

if MOBILE_MODE:
    from android.storage import app_storage_path  # pylint: disable=import-error # type: ignore
    PATH_APP_FOLDER = app_storage_path() + "/"
else:
    PATH_APP_FOLDER = "./"


# Path for the folders
PATH_RESOURCES_FOLDER = "resources/"

# Path for the user data
PATH_USER_DATA = PATH_APP_FOLDER + "data.json"

# Path for the screen
PATH_SCREENS = "screens/"

# Path for the resources
PATH_LANGUAGE = PATH_RESOURCES_FOLDER + "languages/"
PATH_IMAGES = PATH_RESOURCES_FOLDER + "images/"
PATH_MAP_TEXTURES = PATH_IMAGES + "map_textures/"
PATH_ATLAS = PATH_RESOURCES_FOLDER + "atlas/"
PATH_MAPS = PATH_RESOURCES_FOLDER + "maps/"
PATH_SOUNDS = PATH_RESOURCES_FOLDER + "sounds/"
PATH_MUSICS = PATH_RESOURCES_FOLDER + "musics/"
PATH_FONTS = PATH_RESOURCES_FOLDER + "fonts/"
PATH_GAMEPLAY = PATH_RESOURCES_FOLDER + "gameplay.json"
PATH_IMAGES_TUTORIAL = PATH_IMAGES + "tutorial_"

# Path for the fonts
PATH_TITLE_FONT = PATH_FONTS + "scratched_letters_V2.ttf"
PATH_TEXT_FONT = PATH_FONTS + "Aquifer.ttf"

# Path for the backgrounds
if IS_WINTER:
    PATH_MENU_BACKGROUND = PATH_IMAGES + "menu_background_christmas.jpg"
    PATH_DAY_CAMP_BACKGROUND = PATH_IMAGES + "day_camp_christmas.jpg"
    PATH_NIGHT_CAMP_BACKGROUND = PATH_IMAGES + "night_camp_christmas.jpg"
else:
    PATH_MENU_BACKGROUND = PATH_IMAGES + "menu_background.jpg"
    PATH_DAY_CAMP_BACKGROUND = PATH_IMAGES + "day_camp.jpg"
    PATH_NIGHT_CAMP_BACKGROUND = PATH_IMAGES + "night_camp.jpg"
