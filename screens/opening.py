"""
Module for the opening screen.
"""

###############
### Imports ###
###############

import os
from threading import Thread
from tools.kivy_tools import ImprovedScreen
from tools.path import (
    PATH_RESOURCES_FOLDER,
    PATH_TEXT_FONT
)
from kivy.clock import Clock
from kivy.lang import Builder


class OpeningScreen(ImprovedScreen):
    """
    Screen of Opening.
    """

    def __init__(self, **kw):
        super().__init__(
            font_name=PATH_TEXT_FONT,
            back_image_path=PATH_RESOURCES_FOLDER + "logo_roadsign.png",
            **kw)

    def on_enter(self, *args):
        print("enter opening screen")
        # Schedule preload of the game screen
        thread = Thread(target=self.load_kv_files)
        thread.start()
        return super().on_enter(*args)

    # def switch_to_menu(self, *args):
    #     self.manager.current = "menu"

    def load_kv_files(self, *_):
        print("load the screens")
        from screens import (
            MenuScreen,
            GameScreen,
            SettingsScreen,
            GameOverScreen,
            AchievementsScreen,
            TutorialScreen)

        kv_files = [file for file in os.listdir(
            "screens") if file.endswith(".kv")]
        for file in kv_files:
            Builder.load_file(f"screens/{file}", encoding="utf-8")

        self.MenuScreen = MenuScreen
        self.GameScreen = GameScreen
        self.SettingsScreen = SettingsScreen
        self.GameOverScreen = GameOverScreen
        self.AchievementsScreen = AchievementsScreen
        self.TutorialScreen = TutorialScreen

        Clock.schedule_once(self.load_other_screens)

    def load_other_screens(self, *args):

        ### Load the kv files of the screens ###
        menu_screen = self.MenuScreen(name="menu")
        self.manager.add_widget(menu_screen)
        game_screen = self.GameScreen(name="game")
        self.manager.add_widget(game_screen)
        settings_screen = self.SettingsScreen(name="settings")
        self.manager.add_widget(settings_screen)
        game_over_screen = self.GameOverScreen(name="game_over")
        self.manager.add_widget(game_over_screen)
        achievements_screen = self.AchievementsScreen(name="achievements")
        self.manager.add_widget(achievements_screen)
        tutorial_screen = self.TutorialScreen(name="tutorial")
        self.manager.add_widget(tutorial_screen)
        # Preload screens
        Clock.schedule_once(self.manager.get_screen("game").preload)
        Clock.schedule_once(self.manager.get_screen("game_over").preload)
        self.manager.current = "menu"
