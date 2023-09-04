"""

"""


###############
### Imports ###
###############

### Python imports ###

from math import sin, cos, asin, acos, sqrt, pi, pow, ceil

### Kivy imports ###

from kivy.graphics import Rectangle, Color, Line
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

### Module imports ###

from tools.tools_constants import (
    Window
)


def change_window_size(*args):
    global WINDOW_SIZE, SCREEN_RATIO

    # Compute the size of one tile in pixel
    WINDOW_SIZE = Window.size
    SCREEN_RATIO = WINDOW_SIZE[0] / WINDOW_SIZE[1]


Window.bind(on_resize=change_window_size)
change_window_size()


def apply_boundaries(x, min_x, max_x):
    if x > max_x:
        return max_x
    if x < min_x:
        return min_x
    return x


def norm(x, y):
    return sqrt(pow(x, 2) + pow(y, 2))


TRANSPARENT_WHITE = Color(1.0, 1.0, 1.0, .5)
HIGH_TRANSPARENT_WHITE = Color(1.0, 1.0, 1.0, .3)

#####################################
### Classes for controls on mobil ###
#####################################


class MobileJoystick():
    def __init__(self, layout: RelativeLayout):
        self.center_x = 0.15
        self.center_y = 0.2
        self.width = 0.12
        self.height = 0.12
        self.extension_factor = 2
        self.is_active = False
        self.widget = Widget(pos_hint={"center_x": self.center_x, "center_y": self.center_y}, size_hint=(
            self.width * self.extension_factor, self.height * self.extension_factor * SCREEN_RATIO))
        layout.add_widget(self.widget)
        self.back_to_zero()
        self.widget.bind(on_touch_move=self.on_touch_move)
        self.widget.bind(on_touch_down=self.on_touch_down)
        self.widget.bind(on_touch_up=self.on_touch_up)
        self.draw()

    def on_touch_move(self, el, touch):
        if touch.x < WINDOW_SIZE[0] // 2:
            self.x = touch.x
            self.y = touch.y

    def on_touch_down(self, el, touch):
        if touch.x < WINDOW_SIZE[0] // 2:
            self.is_active = True

    def on_touch_up(self, el, touch):
        if touch.x < WINDOW_SIZE[0] // 2:
            self.is_active = False
            self.back_to_zero()
            self.draw()

    def back_to_zero(self):
        self.x = self.center_x * WINDOW_SIZE[0]
        self.y = self.center_y * WINDOW_SIZE[1]

    def draw(self):
        self.widget.pos_hint = {
            "center_x": self.center_x, "center_y": self.center_y}
        self.widget.size_hint = (self.width * self.extension_factor,
                                 self.height * self.extension_factor * SCREEN_RATIO)
        self.widget.canvas.clear()
        # Réglage de la couleur
        self.widget.canvas.add(TRANSPARENT_WHITE)
        # Affichage du cercle extérieur
        self.main_center_x = self.center_x * WINDOW_SIZE[0]
        self.main_center_y = self.center_y * WINDOW_SIZE[1]
        main_radius = self.width * WINDOW_SIZE[1]
        self.norme_cercle = main_radius
        self.widget.canvas.add(
            Line(circle=(self.main_center_x, self.main_center_y, main_radius), width=5))
        # Affichage du cercle intérieur
        max_x = self.main_center_x + main_radius
        min_x = self.main_center_x - main_radius
        self.in_center_x = apply_boundaries(self.x, min_x, max_x)
        max_y = self.main_center_y + main_radius
        min_y = self.main_center_y - main_radius
        self.in_center_y = apply_boundaries(self.y, min_y, max_y)
        in_radius = main_radius // 2
        self.widget.canvas.add(
            Line(circle=(self.in_center_x, self.in_center_y, in_radius), width=3))

    def get_direction(self):
        if not (self.is_active):
            return 0, 0
        else:
            diff_x = apply_boundaries(
                self.x - self.main_center_x, -self.norme_cercle, self.norme_cercle)
            diff_y = apply_boundaries(
                self.y - self.main_center_y, -self.norme_cercle, self.norme_cercle)
            norme = norm(diff_x, diff_y)
            if norme > 0:
                return diff_x / norme, diff_y / norme
            else:
                return 0, 0

    def recursive_update(self):
        self.draw()


class MobileButton():
    def __init__(self, layout: RelativeLayout):
        self.center_x = 0.85
        self.center_y = 0.2
        self.width = 0.12
        self.height = 0.12
        self.extension_factor = 2
        self.is_active = False
        self.last_state = True
        self.widget = Widget(pos_hint={"center_x": self.center_x, "center_y": self.center_y}, size_hint=(
            self.width * self.extension_factor, self.height * self.extension_factor * SCREEN_RATIO))
        layout.add_widget(self.widget)
        self.widget.bind(on_touch_move=self.on_touch_move)
        self.widget.bind(on_touch_down=self.on_touch_down)
        self.widget.bind(on_touch_up=self.on_touch_up)
        self.draw()

    def get_state(self):
        return self.is_active

    def on_touch_move(self, el, touch):
        if touch.x > WINDOW_SIZE[0] // 2:
            if self.widget.collide_point(touch.x, touch.y):
                self.is_active = True
            else:
                self.is_active = False

    def on_touch_down(self, el, touch):
        if touch.x > WINDOW_SIZE[0] // 2:
            if self.widget.collide_point(touch.x, touch.y):
                self.is_active = True

    def on_touch_up(self, el, touch):
        if touch.x > WINDOW_SIZE[0] // 2:
            if self.widget.collide_point(touch.x, touch.y):
                self.is_active = False

    def draw(self):
        self.widget.pos_hint = {
            "center_x": self.center_x, "center_y": self.center_y}
        self.widget.size_hint = (self.width * self.extension_factor,
                                 self.height * self.extension_factor * SCREEN_RATIO)
        if self.last_state != self.is_active:
            self.widget.canvas.clear()
            # Réglage de la couleur
            if self.is_active == True:
                self.widget.canvas.add(HIGH_TRANSPARENT_WHITE)
            else:
                self.widget.canvas.add(TRANSPARENT_WHITE)
            # Affichage du cercle extérieur
            self.main_center_x = self.center_x * WINDOW_SIZE[0]
            self.main_center_y = self.center_y * WINDOW_SIZE[1]
            main_radius = self.width * WINDOW_SIZE[1]
            self.widget.canvas.add(
                Line(circle=(self.main_center_x, self.main_center_y, main_radius), width=5))
        self.last_state = self.is_active

    def recursive_update(self):
        self.draw()
