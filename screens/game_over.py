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
from kivy.core.window import Window

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

if MOBILE_MODE:
    from androidstorage4kivy import SharedStorage, ShareSheet  # type: ignore
    from android.storage import app_storage_path  # type: ignore
    from android.permissions import request_permissions, Permission  # pylint: disable=import-error # type: ignore


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

    def share_score(self):
        if self.share_button:
            print("start sharing")
            if MOBILE_MODE:
                request_permissions(
                    [Permission.READ_FRAME_BUFFER, Permission.CAPTURE_VIDEO_OUTPUT, Permission.CAPTURE_SECURE_VIDEO_OUTPUT])
            # Save the screenshot
            if os.path.exists("screenshot0001.png"):
                os.remove("screenshot0001.png")
            # self.ids["share_button"].opacity = 0
            # self.ids["back_button"].opacity = 0
            print("hiding finished")
            Window.screenshot("screenshot.png")
            print("screenshot taken")
            # self.ids["share_button"].opacity = 1
            # self.ids["back_button"].opacity = 1
            # print("redisplay buttons")

            if MOBILE_MODE:
                # Copy it into the shared storage
                print("save in shared storage")
                shared_storage = SharedStorage()
                PATH_APP_FOLDER = app_storage_path()
                print(os.listdir("."))
                print(os.listdir(PATH_APP_FOLDER))
                file_to_share = shared_storage.copy_to_shared(
                    "screenshot0001.png", filepath="/screenshot0001.png")
                # Share it
                print("share the image")
                shared_sheet = ShareSheet()
                shared_sheet.share_file(file_to_share)
