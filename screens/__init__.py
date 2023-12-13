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
from screens.intermediate_menu import IntermediateMenuScreen
from screens.settings import SettingsScreen
from screens.game import GameScreen
from screens.game_over import GameOverScreen
from screens.achievements import AchievementsScreen
from screens.tutorial import TutorialScreen
from screens.help import HelpScreen
