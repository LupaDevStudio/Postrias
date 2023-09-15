"""
Module for the collection menu
"""

###############
### Imports ###
###############

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import StringProperty
from tools.path import (
    PATH_TEXT_FONT,
    PATH_IMAGES
)
from tools.constants import (
    USER_DATA,
    TEXT,
    TEXT_FONT_COLOR
)
from tools.kivy_tools import ImprovedScreen

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
            back_image_path=PATH_IMAGES + "collection_background.png",
            **kw)

    my_highscore = StringProperty("")
    number_cols = 3
    spacing = Window.size[0] / 50
    padding = [0.05 * Window.size[0], 0, 0.05 * Window.size[0], 0]

    def on_enter(self, *args):
        self.ids.my_sv_layout.reset_screen()
        self.my_highscore = TEXT.game_over["highscore"] + \
            str(USER_DATA.highscore)
        self.on_resize()
        self.build_scroll_view()
        return super().on_enter(*args)

    def on_resize(self, *args):
        self.spacing = Window.size[0] / 50
        return super().on_resize(*args)

    def go_to_menu(self):
        """
        Go back to the main menu.
        """
        self.manager.current = "menu"

    def build_scroll_view(self):

        for (code_ending, bool_ending) in USER_DATA.endings.items():
            relative_layout = RelativeLayout(
                size_hint=(1, 1),
                # height=height_layout,
                # width=self.image_dimension
            )

            path_image = PATH_IMAGES + "ending_unknown.png"
            title_ending = "???"
            if bool_ending:
                path_image = PATH_IMAGES + "ending_" + code_ending + ".png"
                title_ending = TEXT.ending[code_ending]["title"]

            name_label = Button(
                # width=self.image_dimension,
                size_hint=(1, 0.1),
                # color=TEXT_FONT_COLOR,
                text=title_ending,
                pos_hint={"x": 0, "y": 0},
                # font_name=self.font_name,
                # font_size=25 * self.font_ratio
            )
            relative_layout.add_widget(name_label)

            # Image
            image = Image(
                source=path_image,
                size_hint=(1, 0.9),
                # width=self.image_dimension,
                # height=self.image_dimension,
                allow_stretch=True,
                keep_ratio=False,
                pos_hint={"x": 0, "y": 0.1}
            )
            relative_layout.add_widget(image)
            self.ids.my_sv_layout.add_widget(relative_layout)
