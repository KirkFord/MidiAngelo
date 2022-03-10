import os
import re
from midi2audio import FluidSynth
from pydub import AudioSegment

"""
soundfont_name = sys.argv[1]
midi_in_name = sys.argv[2]
wav_output_name = sys.argv[3]
#this section has the actual MIDI to .wav/.flac
# within the fluidsynth param you put the name/path of the sf2 (soundfont)
# midi_to_audio takes a midi file as the first parameter and the name of the output file as the second parameter.
# if we use .flac the file size is much around 14x smaller than a .wav file. mp3s are not supported through this (to my knowledge)
FluidSynth('soundfonts/' + str(soundfont_name)).midi_to_audio(midi_in_name, wav_output_name)
"""


def createWav(midi_in_name, soundfont_name, wav_output_name, db_boost=0):
    if db_boost != 0:
        temp_wav_name = "temp_" + wav_output_name
        FluidSynth(str(soundfont_name)).midi_to_audio(midi_in_name, temp_wav_name)

        volume = int(db_boost)
        song = AudioSegment.from_wav(temp_wav_name)
        if volume > 0:
            volume_song = song + volume
        elif volume < 0:
            volume_song = song - abs(volume)
        volume_song.export(wav_output_name, format="wav")
    else:
        FluidSynth(str(soundfont_name)).midi_to_audio(midi_in_name, wav_output_name)


def find_deleteable():
    os.remove("first_sound.wav")
    os.remove("second_sound.wav")
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if re.search('combined.+', f):
            os.remove(f)
        elif re.search("sound.+", f):
            os.remove(f)


# do something
# soundfount list is a LIST [] of all the font names we want to combine.
# each item in the list needs to have a full .sf2 name
def overlayWavs(soundfont_list, midi_in_name, wav_output_name, db_boost=0):
    number_of_overlays = len(soundfont_list)
    # first sound created
    createWav(midi_in_name, soundfont_list[0], "first_sound.wav", db_boost)
    sound1 = AudioSegment.from_file("first_sound.wav")
    # second sound created
    createWav("however_you_pass_this.mid", soundfont_list[1], "second_sound.wav", db_boost)
    sound2 = AudioSegment.from_file("second_sound.wav")
    # combined sounds
    combined = sound1.overlay(sound2)
    combined.export("combined2.wav", format='wav')

    # combine the rest of the options in the soundfont list
    if number_of_overlays > 2:
        for i in range(2, number_of_overlays):
            createWav(midi_in_name, soundfont_list[i], "sound" + str(i) + ".wav", db_boost)
            combined_sound = AudioSegment.from_file("combined" + str(i) + ".wav")
            sound_added = AudioSegment.from_file("sound" + str(i) + ".wav")
            combined_loop = combined_sound.overlay(sound_added)
            combined_loop.export("combined" + str(i + 1) + ".wav", format='wav')
    # rename the file into the parameter passed in
    old_name = "combined" + str(number_of_overlays) + ".wav"
    new_name = str(wav_output_name)
    os.rename(old_name, new_name)
    find_deleteable()
