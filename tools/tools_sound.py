"""
Module to manage musics and sound effects
"""

###############
### Imports ###
###############

import os

from math import exp

from kivy.core.audio import SoundLoader

from tools.tools_constants import (
    FPS,
    SOUND_VOLUME,
    MUSIC_VOLUME,
    PATH_SOUNDS,
    PATH_MUSICS
)

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

    def change_volume(self, name, new_volume):
        self.musics[name].volume = new_volume

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

    def __init__(self, dict_music):
        super().__init__(dict_music)
        self.instructions = []
        dico_frame_state = {}
        for key in dict_music:
            dico_frame_state[key] = 0
        self.dico_frame_state = dico_frame_state

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
                fade_diff = SOUND_VOLUME / frame_to_fade
                new_volume = volume - fade_diff
            elif instruction[0] == "exp_fade_out":
                key, duration = instruction[1], instruction[2]
                frame_to_fade = FPS * duration
                t = 60 * self.dico_frame_state[key] / frame_to_fade
                self.dico_frame_state[key] += 1
                new_volume = exp_fade_out(t) * SOUND_VOLUME
            # Application du changement de volume
            if new_volume is not None:
                if new_volume > 0:
                    self.musics[key].volume = new_volume
                else:
                    self.musics[key].volume = 0
                    self.musics[key].stop()
                    self.musics[key].volume = SOUND_VOLUME
                    self.dico_frame_state[key] = 0
                    pop_list.append(instruction)
        # Enlève les instructions terminées
        for el in pop_list:
            self.instructions.remove(el)

class SoundMixer():
    """
    Classe destinée à gérer les bruitages dans le jeu
    Elle est capable de jouer plusieurs fois le même son en même temps
    """

    def __init__(self, dict_sound, volume, sound_limit=10):
        self.sounds = {}
        self.sound_limit = sound_limit
        for key in dict_sound:
            self.sounds[key] = [SoundLoader.load(dict_sound[key])
                                for i in range(sound_limit)]
            for i in range(sound_limit):
                self.sounds[key][i].volume = volume

    def play(self, name):
        i = 0
        while i < self.sound_limit and self.sounds[name][i].state == "play":
            i += 1
        if i < self.sound_limit:
            self.sounds[name][i].play()
        else:
            print("Unable to play the desired sound, channel saturation")

#################
### Functions ###
#################

def exp_fade_out(t):
    return 1 - exp((t - 60) * 0.15)


def load_sounds(folder, volume):
    """Fonction pour charger tous les sons d'un coup.
    Prend en entrée un dictionnaire avec le nom de chaque son et sa position.
    Renvoie un dictionnaire avec le nom de chaque son et le son lui-même.
    """
    dico = {}
    for file in os.listdir(folder):
        name_file = file.split(".")[0]
        dico[name_file] = SoundLoader.load(folder + file)
        dico[name_file].volume = volume
    return dico

###############
### Process ###
###############


# Load the dictionnaries
MUSIC_DICT = load_sounds(PATH_MUSICS, MUSIC_VOLUME)
SOUND_DICT = load_sounds(PATH_SOUNDS, SOUND_VOLUME)

# Create the mixer
music_mixer = DynamicMusicMixer(MUSIC_DICT)
sound_mixer = DynamicMusicMixer(SOUND_DICT)
