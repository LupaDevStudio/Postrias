"""
Module for the collection menu
"""

# TODO
# Fins débloquées
# Highscore

###############
### Imports ###
###############


from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from tools.tools_constants import (
    PATH_TITLE_FONT,
    PATH_IMAGES
)


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


class AchievementsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    font = PATH_TITLE_FONT
    path_images = PATH_IMAGES
    counter_precious_stones = StringProperty("")
    number_cols = 7
    spacing = global_spacing["horizontal"]
    label_height = 40 * 7 * Window.size[1] / 2340
    padding = [0.05 * Window.size[0], 0, 0.05 * Window.size[0], 0]
    path_back_image = PATH_IMAGES + "collection_background.png"
    font_ratio = NumericProperty(0)
    width_back_image = ObjectProperty(Window.size[0])
    height_back_image = ObjectProperty(Window.size[0] * 392 / 632)

    def init_screen(self):
        pass
        # self.font_ratio = Window.size[0]/800
        # self.width_back_image = Window.size[0]
        # self.height_back_image = Window.size[0] * 392 / 632
        # self.label_height = 40 * 7 * Window.size[1] / 2340
        # self.padding = [0.05 * Window.size[0], 0, 0.05 * Window.size[0], 0]
        # self.ids.my_sv_layout.reset_screen()
        # number_precious_stones = 0
        # for stone in my_collection.dict_collection:
        #     if my_collection.dict_collection[stone]:
        #         number_precious_stones += 1
        # number_total_precious_stones = len(
        #     my_collection.dict_collection.keys())
        # self.counter_precious_stones = str(number_precious_stones) + " / " + str(
        #     number_total_precious_stones)
        # self.build_scroll_view()

    # def build_scroll_view(self):
    #     TEXTURE_DICT = load_textures_from_atlas("map_textures")
    #     image_dimension = (Window.size[0] - 2 * self.padding[0] - self.spacing * (
    #         self.number_cols - 1)) / self.number_cols
    #     height_layout = image_dimension + self.label_height
    #     for code_precious_stone in DICT_TREASURE_STONES:
    #         name_image = DICT_TREASURE_STONES[code_precious_stone]
    #         if my_collection.dict_collection[name_image]:
    #             relative_layout = RelativeLayout(
    #                 size_hint=(None, None),
    #                 height=height_layout,
    #                 width=image_dimension
    #             )
    #             # Label for the name of the gallery
    #             name_displayed = name_image
    #             if name_image == "Tiger eye":
    #                 name_displayed = "Tiger's eye"
    #             name_label = Label(
    #                 size_hint=(None, None),
    #                 width=image_dimension,
    #                 height=self.label_height,
    #                 color=self.manager.color_label,
    #                 text=name_displayed,
    #                 pos_hint={"x": 0, "y": 0},
    #                 font_name=self.font,
    #                 font_size=25*self.font_ratio
    #             )
    #             relative_layout.add_widget(name_label)
    #             # Image
    #             image = Image(
    #                 size_hint=(None, None),
    #                 width=image_dimension,
    #                 height=image_dimension,
    #                 texture=TEXTURE_DICT[DICT_TREASURE_STONES[code_precious_stone]],
    #                 allow_stretch=True,
    #                 y=self.label_height
    #             )
    #             relative_layout.add_widget(image)
    #             self.ids.my_sv_layout.add_widget(relative_layout)
