import sys
from midi2audio import FluidSynth

soundfont_name = sys.argv[1]
midi_in_name = sys.argv[2]
wav_output_name = sys.argv[3]
#this section has the actual MIDI to .wav/.flac
# within the fluidsynth param you put the name/path of the sf2 (soundfont)
# midi_to_audio takes a midi file as the first parameter and the name of the output file as the second parameter.
# if we use .flac the file size is much around 14x smaller than a .wav file. mp3s are not supported through this (to my knowledge)
<<<<<<< Updated upstream
FluidSynth('soundfonts/' + str(soundfont_name)).midi_to_audio(midi_in_name, wav_output_name)
=======
FluidSynth('soundfonts/' + str(soundfont_name)).midi_to_audio(midi_in_name, wav_output_name)
"""


def createWav(midi_in_name, soundfont_name, wav_output_name):
	FluidSynth(str(soundfont_name)).midi_to_audio(midi_in_name, wav_output_name)
>>>>>>> Stashed changes
