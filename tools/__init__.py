"""
Tools package of the application.

Modules
-------

"""

###############
### Imports ###
###############

### Module imports ###

from tools.game_tools import (
    MusicMixer,
    DynamicMusicMixer,
    SoundMixer,
    load_sounds
)

from tools.path import (
    PATH_MUSICS,
    PATH_SOUNDS
)

from tools.constants import (
    USER_DATA
)

# Load the dictionnaries
MUSIC_DICT = load_sounds(PATH_MUSICS, USER_DATA["music_volume"])
SOUND_DICT = load_sounds(PATH_SOUNDS, USER_DATA["sound_effects_volume"])

# Create the mixer
music_mixer = DynamicMusicMixer(MUSIC_DICT, USER_DATA["music_volume"])
sound_mixer = DynamicMusicMixer(SOUND_DICT, USER_DATA["sound_effects_volume"])
