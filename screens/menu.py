"""
Module for the main menu
"""


from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ObjectProperty,
    NumericProperty
)

from tools.tools_constants import (
    PATH_IMAGES,
    FPS,
    PATH_TITLE_FONT,
    MOBILE_MODE
)
from tools.tools_sound import music_mixer


class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.opacity_state = -1

    path_images = PATH_IMAGES
    font = PATH_TITLE_FONT
    path_back_image = PATH_IMAGES + "menu_background.png"
    font_ratio = NumericProperty(0)
    width_back_image = ObjectProperty(Window.size[0])
    height_back_image = ObjectProperty(Window.size[0] * 392 / 632)
    mobile_mode = BooleanProperty(True)
    high_score = StringProperty("")

    def init_screen(self):
        self.mobile_mode = MOBILE_MODE
        self.font_ratio = Window.size[0] / 800
        self.width_back_image = Window.size[0]
        self.height_back_image = Window.size[0] * 392 / 632
        if music_mixer.musics["title_music"].state != "play":
            music_mixer.play("title_music", loop=True)

        try:
            if MOBILE_MODE:
                self.remove_widget(self.ids.settings_logo)
                self.remove_widget(self.ids.settings_button)
            else:
                self.remove_widget(self.ids.high_score_label)
        except:
            pass

        try:
            Clock.unschedule(self.update)
        except:
            pass
        Clock.schedule_interval(self.update, 1 / FPS)

    def update(self, *args):
        self.ids.start_label.opacity += self.opacity_state * OPACITY_RATE
        if self.ids.start_label.opacity < 0 or self.ids.start_label.opacity > 1:
            self.opacity_state = -self.opacity_state
