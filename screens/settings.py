"""
Module for the settings menu
"""

# TODO
# Changement de langue (fr en)
# Réglage volume musique bruitage
# Désactiver les pubs


from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.core.window import Window
from tools.path import (
    PATH_TITLE_FONT,
    PATH_IMAGES
)


class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    path_images = PATH_IMAGES
    font = PATH_TITLE_FONT
    high_score = StringProperty("")
    top_key = StringProperty()
    left_key = StringProperty("")
    bottom_key = StringProperty("")
    right_key = StringProperty("")
    interact_key = StringProperty("")
    path_back_image = PATH_IMAGES + "settings_background.png"
    font_ratio = NumericProperty(0)
    width_back_image = ObjectProperty(Window.size[0])
    height_back_image = ObjectProperty(Window.size[0] * 392 / 632)

    def init_screen(self):
        self.font_ratio = Window.size[0] / 800
        self.width_back_image = Window.size[0]
        self.height_back_image = Window.size[0] * 392 / 632
        pass
