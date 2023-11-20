"""
Module for the game over screen
"""

from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from tools.kivy_tools import ImprovedScreen
from tools.path import (
    PATH_IMAGES,
    PATH_TEXT_FONT
)
from tools import (
    music_mixer,
    game
)
from tools.constants import (
    TEXT,
    USER_DATA
)


class GameOverScreen(ImprovedScreen):
    """
    Screen of Game Over.
    """

    ending_text = StringProperty()
    credits_text = StringProperty()
    score_text = StringProperty()
    title_text = StringProperty()

    def __init__(self, **kw):
        super().__init__(
            font_name=PATH_TEXT_FONT,
            **kw)
        self.credits_text = TEXT.game_over["credits"]
        self.new_highscore: bool

    def on_enter(self, *args):
        # Play the game over music
        music_mixer.play("time_of_the_apocalypse")

        # Load the ending text
        self.ending_text = game.ending_text

        # Set the background
        self.set_back_image_path(
            PATH_IMAGES + "ending_" + game.ending + ".jpg")

        if game.score > USER_DATA.highscore:
            self.new_highscore = True
            USER_DATA.highscore = game.score
        else:
            self.new_highscore = False

        self.score_text = TEXT.game_over["score"] + str(game.score) + "\n\n" + \
            TEXT.game_over["highscore"] + str(USER_DATA.highscore)

        if game.score == 0:
            self.ids["score_label"].opacity = 0
            self.back_destination = "achievements"
            self.title_text = TEXT.ending[game.ending]["title"]
        else:
            self.ids["score_label"].opacity = 1
            self.back_destination = "menu"
            self.title_text = "Game Over"

        # Display something when getting a new highscore
        return super().on_enter(*args)

    def on_leave(self, *args):

        # Unlock the end in the achievements menu
        USER_DATA.endings[game.ending] = True

        # Save the changes
        USER_DATA.save_changes()

        return super().on_leave(*args)

    def back_to_menu(self):
        """
        Go back to the main menu
        """
        self.manager.current = self.back_destination
