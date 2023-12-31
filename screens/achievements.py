"""
Module for the collection menu
"""

###############
### Imports ###
###############

from functools import partial
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from tools.path import (
    PATH_TEXT_FONT,
    PATH_IMAGES
)
from tools.constants import (
    USER_DATA,
    TEXT,
    TEXT_FONT_COLOR
)
from tools import (
    music_mixer,
    game
)
from tools.kivy_tools import ImprovedScreen, ImageWithTextButton

################
### Constant ###
################

global_spacing = {
    "horizontal": Window.size[0] / 50,
    "vertical": Window.size[1] / 50
}

#############
### Class ###
#############


class AchievementsScreen(ImprovedScreen):
    def __init__(self, **kw):
        super().__init__(
            font_name=PATH_TEXT_FONT,
            back_image_path=PATH_IMAGES + "collection_background.jpg",
            **kw)
        self.scroll_view_content = {}

    my_highscore = StringProperty("")
    number_cols = 3
    spacing = Window.size[0] / 50
    padding = [0.05 * Window.size[0], 0, 0.05 * Window.size[0], spacing]
    image_dimension = NumericProperty()
    height_layout = NumericProperty()

    def on_enter(self, *args):
        self.ids.my_sv_layout.reset_screen()
        self.my_highscore = TEXT.game_over["highscore"] + \
            str(USER_DATA.highscore)
        self.on_resize()
        music_mixer.play("my_office")
        return super().on_enter(*args)

    def on_resize(self, *args):
        self.spacing = Window.size[0] / 50
        self.image_dimension = (Window.size[0] - 2 * self.padding[0] - self.spacing * (
            self.number_cols - 1)) / self.number_cols
        self.height_layout = self.image_dimension + self.spacing
        self.build_scroll_view()
        return super().on_resize(*args)

    def go_to_menu(self):
        """
        Go back to the main menu.
        """
        self.manager.current = "menu"

    def display_ending(self, ending_code, *args):
        """
        Go to the game over menu and display the ending.
        """
        if USER_DATA.endings[ending_code]:
            game.ending_text = TEXT.ending[ending_code]["text"]
            game.score = 0
            game.ending = ending_code
            self.manager.current = "game_over"

    def build_scroll_view(self):
        self.ids.my_sv_layout.reset_screen()

        for (ending_code, bool_ending) in USER_DATA.endings.items():
            relative_layout = RelativeLayout(
                size_hint=(None, None),
                height=self.height_layout,
                width=self.image_dimension
            )

            path_image = PATH_IMAGES + "ending_unknown.png"
            title_ending = "???"
            if bool_ending:
                path_image = PATH_IMAGES + "ending_" + ending_code + ".jpg"
                title_ending = TEXT.ending[ending_code]["title"]

            label = Button(
                width=self.image_dimension,
                size_hint=(0.8, 0.1),
                text=title_ending,
                pos_hint={"center_x": 0.5, "y": 0},
                on_release=partial(self.display_ending, ending_code),
                font_name=self.font_name,
                font_size=15*self.font_ratio
            )
            relative_layout.add_widget(label)

            # Image
            image = Image(
                source=path_image,
                size_hint=(0.7, 0.7),
                width=self.image_dimension,
                height=self.image_dimension,
                allow_stretch=True,
                keep_ratio=False,
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            )
            relative_layout.add_widget(image)

            # Frame
            frame = Image(
                source=PATH_IMAGES + "collection_frame.png",
                size_hint=(0.8, 0.8),
                width=self.image_dimension,
                height=self.image_dimension,
                allow_stretch=True,
                keep_ratio=False,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
            relative_layout.add_widget(frame)

            frame_button = Button(
                on_release=partial(self.display_ending, ending_code),
                size_hint=(0.8, 0.8),
                width=self.image_dimension,
                height=self.image_dimension,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                opacity=0
            )
            relative_layout.add_widget(frame_button)

            # Add the layout
            self.ids.my_sv_layout.add_widget(relative_layout)

            # Store the widgets
            self.scroll_view_content[ending_code] = {}
            self.scroll_view_content[ending_code]["label"] = label
            self.scroll_view_content[ending_code]["image"] = image
            self.scroll_view_content[ending_code]["frame"] = frame
