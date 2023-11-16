"""
Module for the settings menu
"""

# TODO
# Changement de langue (fr en)
# Réglage volume musique bruitage
# Désactiver les pubs
# Revoir le tutoriel

# from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty, NumericProperty, ListProperty
from tools.path import (
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
    TEXT,
    __version__
)
from tools import (
    music_mixer,
    sound_mixer
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
    tutorial_label = StringProperty()
    version_label = StringProperty()

    sound_volume_value = NumericProperty(0.5)
    music_volume_value = NumericProperty(0.5)

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "settings_background.jpg",
            font_name=PATH_TEXT_FONT,
            **kw)

    def load_labels(self):
        """
        Load the text labels of the screen.
        """
        self.sound_volume_label = TEXT.settings["sound_volume"]
        self.music_volume_label = TEXT.settings["music_volume"]
        self.apply_label = TEXT.settings["apply"]
        self.language_label = TEXT.settings["language"]
        self.validate_label = TEXT.settings["validate"]
        self.tutorial_label = TEXT.settings["tutorial"]
        self.version_label = TEXT.settings["version"] + __version__

    def on_enter(self, *args):
        # Load the labels
        self.load_labels()
        # Set the values of the language spinner
        self.values_language_list = LANGUAGES_LIST
        return super().on_enter(*args)

    def change_language(self, language_name):
        """
        Change the language of the game interface.

        Parameters
        ----------
        language_name : str
            Name of the language.
        """
        language_code = DICT_LANGUAGE_NAME_TO_CODE[language_name]
        USER_DATA.language = language_code
        TEXT.change_language(language_code)
        self.load_labels()

    def go_to_menu(self):
        """
        Go back to the main menu.
        """

        self.manager.current = "menu"

    def apply_music_settings(self):
        """
        Apply the music settings choosed by the user using the sliders.
        """

        music_mixer.change_volume(self.music_volume_value)
        sound_mixer.change_volume(self.sound_volume_value)

        USER_DATA.music_volume = self.music_volume_value
        USER_DATA.sound_effects_volume = self.sound_volume_value

    def watch_tutorial(self):
        # TODO
        pass
