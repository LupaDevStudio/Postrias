"""
Main module of the generator of dialogs.
"""


###############
### Imports ###
###############


### Python imports ###

import os
import platform
os_name = platform.system()
if os_name == "Windows":
    os.environ['KIVY_TEXT'] = 'pil'

### Kivy imports ###

# Remove the red dots when right-clicking
from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window


### Ads imports ###

from kivy.utils import platform
if platform == "android":
    from kivads import (
        BannerAd,
        InterstitialAd,
        KivAds,
        RewardedAd,
        RewardedInterstitial,
        TestID,
    )

### Module imports ###

from tools.path import (
    PATH_IMAGES
)
from tools.constants import (
    MOBILE_MODE,
    FPS,
    MSAA_LEVEL
)
from screens import (   # pylint: disable=unused-import
    MenuScreen,
    GameScreen,
    SettingsScreen,
    GameOverScreen,
    AchievementsScreen
)


###############
### General ###
###############


class WindowManager(ScreenManager):
    """
    Screen manager, which allows the navigation between the different menus.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.add_widget(Screen(name="opening"))
        self.current = "opening"
        self.list_former_screens = []


class MainApp(App, Widget):
    """
    Main class of the application.
    """

    def build_config(self, config):
        """
        Build the config file for the application.

        It sets the FPS number and the antialiasing level.
        """
        config.setdefaults('graphics', {
            'maxfps': str(FPS),
            'multisamples': str(MSAA_LEVEL)
        })

    def build(self):
        """
        Build the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        Window.clearcolor = (0, 0, 0, 1)
        self.icon = PATH_IMAGES + "logo.png"
        # self.ads = KivAds()
        # self.interstitial = InterstitialAd(TestID.INTERSTITIAL)
        # self.banner = BannerAd(TestID.BANNER, int(Window.width))
        # self.reward = RewardedAd(TestID.REWARD, self.reward_callback)
        # self.reward_interstitial = RewardedInterstitial(
        #     TestID.REWARD_INTERSTITIAL, self.reward_callback
        # )

    # def reward_callback(self, *args):
    #     print("ADS REWARD")

    def on_start(self):
        if MOBILE_MODE:
            Window.update_viewport()

        # Open the menu screen
        self.root_window.children[0].current = "menu"

        return super().on_start()


# Run the application
if __name__ == "__main__":
    MainApp().run()
