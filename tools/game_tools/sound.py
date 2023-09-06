"""
Module to manage musics and sound effects
"""

###############
### Imports ###
###############

import os

from math import exp

from kivy.core.audio import SoundLoader

from tools.tools_constants import FPS


###############
### Classes ###
###############


class MusicMixer():
    """
    Classe destinée à gérer la musique dans le jeu
    Une seule musique peut être jouée à la fois.
    """

    def __init__(self, dict_music):
        self.musics = dict_music

    def change_volume(self, new_volume, name=None):
        if name is not None:
            self.musics[name].volume = new_volume
        else:
            for key in self.musics:
                self.musics[key].volume = new_volume

    def play(self, name, loop=False, timecode=0, stop_other_sounds=True):
        if stop_other_sounds:
            self.stop()
        self.musics[name].play()
        if timecode != 0:
            # Ne marche pas
            self.musics[name].seek(1)
        self.musics[name].loop = loop

    def stop(self):
        for key in self.musics:
            if self.musics[key].state == "play":
                self.musics[key].stop()


class DynamicMusicMixer(MusicMixer):
    """
    Classe destinée à jouer des bruitages sur lesquels on peut appliquer des effets en jeu.
    """

    def __init__(self, dict_music, volume):
        super().__init__(dict_music)
        self.instructions = []
        dico_frame_state = {}
        for key in dict_music:
            dico_frame_state[key] = 0
        self.dico_frame_state = dico_frame_state
        self.volume = volume

    def fade_out(self, name, duration, mode="linear"):
        if mode == "exp":
            self.instructions.append(("exp_fade_out", name, duration))
        else:
            self.instructions.append(("fade_out", name, duration))

    def recursive_update(self):
        pop_list = []
        # Parcours des instructions à effectuer
        for instruction in self.instructions:
            new_volume = None
            # Calcul de l'instruction
            if instruction[0] == "fade_out":
                key, duration = instruction[1], instruction[2]
                volume = self.musics[key].volume
                frame_to_fade = FPS * duration
                fade_diff = self.volume / frame_to_fade
                new_volume = volume - fade_diff
            elif instruction[0] == "exp_fade_out":
                key, duration = instruction[1], instruction[2]
                frame_to_fade = FPS * duration
                t = 60 * self.dico_frame_state[key] / frame_to_fade
                self.dico_frame_state[key] += 1
                new_volume = exp_fade_out(t) * self.volume
            # Application du changement de volume
            if new_volume is not None:
                if new_volume > 0:
                    self.musics[key].volume = new_volume
                else:
                    self.musics[key].volume = 0
                    self.musics[key].stop()
                    self.musics[key].volume = self.volume
                    self.dico_frame_state[key] = 0
                    pop_list.append(instruction)
        # Enlève les instructions terminées
        for el in pop_list:
            self.instructions.remove(el)


class SoundMixer():
    """
    Manager for the sound effects of the game.

    It is able to play several times the same sound simultaneously.
    """

    def __init__(self, dict_sound, volume, channel_number=10):
        self.sounds = {}
        self.channel_number = channel_number
        for key in dict_sound:
            self.sounds[key] = [SoundLoader.load(dict_sound[key])
                                for i in range(channel_number)]
            for i in range(channel_number):
                self.sounds[key][i].volume = volume

    def play(self, name: str, volume: float | None = None):
        """
        Play the selected sound.
        """
        i = 0
        while i < self.channel_number and self.sounds[name][i].state == "play":
            i += 1
        if i < self.channel_number:
            if volume is not None:
                self.sounds[name][i].volume = volume
            self.sounds[name][i].play()
        else:
            print("Unable to play the desired sound due to channel saturation")

    def change_volume(self, new_volume: float, name: str | None = None):
        if name is not None:
            for i in range(self.channel_number):
                self.sounds[name][i].volume = new_volume
        else:
            for key in self.musics:
                for i in range(self.channel_number):
                    self.sounds[key][i].volume = new_volume

#################
### Functions ###
#################


def exp_fade_out(t):
    """
    Amplitude function of time for an exponential fade out.
    """
    return 1 - exp((t - 60) * 0.15)


def load_sounds(foldername: str, volume: float) -> dict:
    """
    Load all sounds of a folder at once.

    Parameters
    ----------
    foldername : str
        Name of the folder where the sounds are stored.

    volume : float
        Volume to use to play the sounds by default.

    Returns
    -------
    dict
        Dictionnary with the loaded sounds.
    """
    sound_dict = {}
    for file in os.listdir(foldername):
        name_file = file.split(".")[0]
        sound_dict[name_file] = SoundLoader.load(foldername + file)
        sound_dict[name_file].volume = volume
    return sound_dict
