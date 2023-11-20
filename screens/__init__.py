"""
Package to manage the screens of the application.
"""

###############
### Imports ###
###############

### Python imports ###

import os

### Kivy imports ###

from kivy.lang import Builder

### Module imports ###

from tools.path import PATH_SCREENS
from screens.menu import MenuScreen
from screens.settings import SettingsScreen
from screens.game import GameScreen
from screens.game_over import GameOverScreen
from screens.achievements import AchievementsScreen
from screens.tutorial import TutorialScreen


###############
### Process ###
###############

### Load the kv files of the screens ###

kv_files = [file for file in os.listdir("screens") if file.endswith(".kv")]
for file in kv_files:
    Builder.load_file(f"screens/{file}", encoding="utf-8")
