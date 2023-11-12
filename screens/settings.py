"""
Module for the settings menu
"""

# TODO
# Changement de langue (fr en)
# Réglage volume musique bruitage
# Désactiver les pubs
# Revoir le tutoriel

# from kivy.uix.spinner import Spinner
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
    DICT_LANGUAGE_CORRESPONDANCE,
    DICT_LANGUAGE_NAME_TO_CODE,
    TEXT
)


class SettingsScreen(ImprovedScreen):

    current_language = StringProperty(
        DICT_LANGUAGE_CORRESPONDANCE[USER_DATA.language])
    values_language_list = ListProperty()

    sound_volume_label = StringProperty()
    music_volume_label = StringProperty()
    apply_label = StringProperty()
    language_label = StringProperty()
    disable_ads_label = StringProperty()
    enter_code_label = StringProperty()
    validate_label = StringProperty()

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "settings_background.jpg",
            font_name=PATH_TEXT_FONT,
            **kw)

    def load_labels(self):
        self.sound_volume_label = TEXT.settings["sound_volume"]
        self.music_volume_label = TEXT.settings["music_volume"]
        self.apply_label = TEXT.settings["apply"]
        self.language_label = TEXT.settings["language"]
        self.disable_ads_label = TEXT.settings["disable_ads"]
        self.enter_code_label = TEXT.settings["enter_code"]
        self.validate_label = TEXT.settings["validate"]

    def on_enter(self, *args):
        self.load_labels()
        self.values_language_list = LANGUAGES_LIST
        return super().on_enter(*args)

    def change_language(self, language_name):
        language_code = DICT_LANGUAGE_NAME_TO_CODE[language_name]
        USER_DATA.language = language_code
        TEXT.change_language(language_code)
        self.load_labels()

    def go_to_menu(self):
        """
        Go back to the main menu.
        """
        self.manager.current = "menu"
