"""
Module for the game over screen.
"""

###############
### Imports ###
###############

### Python imports ###

import os

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    BooleanProperty
)
from kivy.clock import Clock


### Module imports ###

from tools.kivy_tools import (
    ImprovedScreen
)
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
    USER_DATA,
    MOBILE_MODE
)
from tools.share_image import (
    create_image_to_share
)

if MOBILE_MODE:
    from androidstorage4kivy import SharedStorage, ShareSheet  # type: ignore
    from android.storage import app_storage_path  # type: ignore
    from tools.kivyreview import request_review


###############
### Classes ###
###############


class GameOverScreen(ImprovedScreen):
    """
    Screen of Game Over.
    """

    ending_text = StringProperty()
    credits_text = StringProperty()
    score_text = StringProperty()
    title_text = StringProperty()
    share_button = BooleanProperty()

    def __init__(self, **kw):
        super().__init__(
            font_name=PATH_TEXT_FONT,
            **kw)
        self.new_highscore: bool

    def on_pre_enter(self, *args):
        # Load the credits sentence
        self.credits_text = TEXT.game_over["credits"]

        # Load the ending text
        self.ending_text = game.ending_text

        # Set the background
        self.set_back_image_path(
            PATH_IMAGES + "ending_" + game.ending + ".jpg")

        # Detect if it is the first game of the player
        if USER_DATA.highscore == 0 and game.score != 0:
            self.is_first_game = True
        else:
            self.is_first_game = False

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
            self.share_button = False
        else:
            self.ids["score_label"].opacity = 1
            self.back_destination = "menu"
            self.title_text = "Game Over"
            self.share_button = True

        return super().on_pre_enter(*args)

    def on_enter(self, *args):

        # Play the game over music
        music_mixer.play("time_of_the_apocalypse")

        # Clear the saved game data
        USER_DATA.saved_data = None
        USER_DATA.save_changes()

        # Display something when getting a new highscore
        return super().on_enter(*args)

    def on_leave(self, *args):

        # Unlock the end in the achievements menu
        USER_DATA.endings[game.ending] = True

        # Save the changes
        USER_DATA.save_changes()

        # Open the in app review window if it is the first game
        if self.is_first_game and MOBILE_MODE:
            Clock.schedule_once(request_review, 1)

        return super().on_leave(*args)

    def go_to_menu(self):
        """
        Go back to the main menu
        """
        self.manager.current = self.back_destination

    def re_enable_share_button(self, *args):
        self.share_button = True

    def share_score(self):
        if self.share_button:
            self.share_button = False
            print("start sharing")
            # Save the screenshot
            if os.path.exists("share_image.png"):
                os.remove("share_image.png")

            create_image_to_share(
                game.score, TEXT.ending[game.ending]["title"], self.back_image_path)
            print("Image created")

            if MOBILE_MODE:
                # Copy it into the shared storage
                print("save in shared storage")
                shared_storage = SharedStorage()
                PATH_APP_FOLDER = app_storage_path()
                print(os.listdir("."))
                print(os.listdir(PATH_APP_FOLDER))
                file_to_share = shared_storage.copy_to_shared(
                    "share_image.png", filepath="/share_image.png")
                # Share it
                print("share the image")
                shared_sheet = ShareSheet()
                shared_sheet.share_file(file_to_share)
            Clock.schedule_once(self.re_enable_share_button, 2)
