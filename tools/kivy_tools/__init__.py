"""
Package containing useful tools and shortcuts for kivy development.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.lang import Builder

### Package imports ###

from tools.kivy_tools.screen import ImprovedScreen
from tools.path import PATH_KIVY_FOLDER

###############
### Process ###
###############


### Kv files ###

# Build the kv file for the custom style
Builder.load_file(PATH_KIVY_FOLDER + "extended_style.kv", encoding="utf-8")

# Build the kv file for screen
Builder.load_file(PATH_KIVY_FOLDER + "screen.kv", encoding="utf-8")
