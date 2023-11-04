"""
Module for the settings menu
"""

# TODO
# Changement de langue (fr en)
# Réglage volume musique bruitage
# Désactiver les pubs

from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from tools.path import (
    PATH_TITLE_FONT,
    PATH_IMAGES,
    PATH_TEXT_FONT
)
from tools.kivy_tools import (
    ImprovedScreen
)
from tools.constants import (
    USER_DATA,
    LANGUAGES_LIST,
    DICT_LANGUAGE_CORRESPONDANCE
)


class SettingsScreen(ImprovedScreen):

    current_language = StringProperty(
        DICT_LANGUAGE_CORRESPONDANCE[USER_DATA.language])
    values_language_list = ListProperty()

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "settings_background.jpg",
            font_name=PATH_TEXT_FONT,
            **kw)

    def on_enter(self, *args):
        print(LANGUAGES_LIST)
        self.values_language_list = LANGUAGES_LIST
        return super().on_enter(*args)

    def go_to_menu(self):
        """
        Go back to the main menu.
        """
        self.manager.current = "menu"
