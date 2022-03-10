import os
import re


from midi2audio import FluidSynth
from pydub import AudioSegment
import ffmpeg

from numpy import number
"""
soundfont_name = sys.argv[1]
midi_in_name = sys.argv[2]
wav_output_name = sys.argv[3]
#this section has the actual MIDI to .wav
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
	return wav_output_name

def find_deleteable():
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	for f in files:
		if re.search("sound.+", f):
			os.remove(f)


def overlayWavs(soundfont_list, midi_in_name, wav_output_name, db_boost=0):
	number_of_overlays = len(soundfont_list)
	sounds = []
	empty = AudioSegment.empty()
	for i in range(number_of_overlays):
		createWav(midi_in_name, soundfont_list[i], "sound" + str(i) + ".wav", db_boost)
		sound_added = AudioSegment.from_wav("sound" + str(i) + ".wav")
		empty += sound_added
	# rename the file into the parameter passed in
	"""
	for sound in sounds:
		empty = empty + sound
	"""
	
	empty[0].export(wav_output_name, format=".wav")
	find_deleteable()
