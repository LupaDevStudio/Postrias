"""
Module for the game over screen
"""


from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window
from tools.tools_constants import (
    PATH_TITLE_FONT,
    PATH_IMAGES,
    FPS,
    OPACITY_RATE
)
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from tools.tools_sound import music_mixer


class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    font = PATH_TITLE_FONT
    path_back_image = PATH_IMAGES + "game_over_background.png"
    width_back_image = ObjectProperty(Window.size[0])
    height_back_image = ObjectProperty(Window.size[0] * 392 / 632)
    opacity_state = - 1
    font_ratio = NumericProperty(0)
    score_str = StringProperty("")

    def init_screen(self, *args):
        self.font_ratio = Window.size[0]/800
        self.width_back_image = Window.size[0]
        self.height_back_image = Window.size[0] * 392 / 632
        music_mixer.play("game_over_music", loop=True)
        score_str = f"Score: {int(args[0])}"
        self.ids.score_label.text = score_str
        Clock.schedule_interval(self.update, 1 / FPS)

    def update(self, *args):
        self.ids.back_to_menu.opacity += self.opacity_state * OPACITY_RATE
        if self.ids.back_to_menu.opacity < 0 or self.ids.back_to_menu.opacity > 1:
            self.opacity_state = -self.opacity_state
