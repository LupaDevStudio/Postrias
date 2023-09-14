"""
Module for the collection menu
"""

###############
### Imports ###
###############

from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import StringProperty
from tools.path import (
    PATH_TITLE_FONT,
    PATH_IMAGES
)
from tools.constants import (
    USER_DATA,
    TEXT
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
            font_name=PATH_TITLE_FONT,
            back_image_path=PATH_IMAGES + "collection_background.png",
            **kw)

    counter_endings = StringProperty("")
    number_cols = 3
    label_height = 0.15 * Window.size[1]
    spacing = global_spacing["horizontal"]
    padding = [0.05 * Window.size[0], 0, 0.05 * Window.size[0], 0]

    def on_enter(self, *args):
        self.ids.my_sv_layout.reset_screen()
        self.build_scroll_view()
        return super().on_enter(*args)

    def test(self):
        print("toto")

    def build_scroll_view(self):
        image_dimension = (Window.size[0] - 2 * self.padding[0] -
                           self.spacing * (self.number_cols - 1)) / self.number_cols
        height_layout = image_dimension + self.label_height
        for code_ending in USER_DATA.endings:
            if USER_DATA.endings[code_ending]:
                relative_layout = RelativeLayout(
                    size_hint=(None, None),
                    height=height_layout,
                    width=image_dimension
                )
                name_label = Label(
                    size_hint=(None, None),
                    width=image_dimension,
                    height=self.label_height,
                    color=self.manager.color_label,
                    text=TEXT.ending[code_ending]["title"],
                    pos_hint={"x": 0, "y": 0},
                    font_name=self.font_name,
                    font_size=25 * self.font_ratio
                )
                relative_layout.add_widget(name_label)
                # Image
                image = Image(
                    source=PATH_IMAGES + "ending_" + code_ending + ".png",
                    size_hint=(None, None),
                    width=image_dimension,
                    height=image_dimension,
                    allow_stretch=True,
                    y=self.label_height
                )
                relative_layout.add_widget(image)
                self.ids.my_sv_layout.add_widget(relative_layout)
