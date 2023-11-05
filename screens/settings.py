"""
Module for the settings menu
"""

# TODO
# Changement de langue (fr en)
# Réglage volume musique bruitage
# Désactiver les pubs
# Revoir le tutoriel


from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.core.window import Window
from tools.path import (
    PATH_TEXT_FONT,
    PATH_IMAGES,
    TEXT
)
from tools.kivy_tools import ImprovedScreen


class SettingsScreen(ImprovedScreen):
    def __init__(self, **kw):
        super().__init__(
            font_name=PATH_TEXT_FONT,
            back_image_path=PATH_IMAGES + "settings_background.png",
            **kw)

    language_label = StringProperty("")

    def on_enter(self):
        super().on_enter()
        self.language_label = TEXT.settings["language"]

    def go_to_menu(self):
        """
        Go back to the main menu.
        """
        self.manager.current = "menu"
