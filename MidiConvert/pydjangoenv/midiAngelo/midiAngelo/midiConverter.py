import music21
from music21 import converter
from midi2audio import FluidSynth

# in this code i have a midi file that is given, i change the tempo of the file and write that tempo to a new file,
# then convert that into a .wav (OR .FLAC!)


# this small section of the code handles the TEMPO CHANGE
# we can scale the tempo of the midi using a "factor" float variable
# where anything over 1 is slower (ie 125% speed, fctr =1.25)
# and anything under 1 is faster (75% speed, fctr =0.75)

fctr = 0.75 # scale (in this case stretch) the overall tempo by this factor
score = music21.converter.parse('/home/ec2-user/pydjangoenv/midiAngelo/midiAngelo/filein.mid')
newscore = score.scaleOffsets(fctr).scaleDurations(fctr)
newscore.write('midi','fileout.mid')

#this section has the actual MIDI to .wav/.flac
# within the fluidsynth param you put the name/path of the sf2 (soundfont)
# midi_to_audio takes a midi file as the first parameter and the name of the output file as the second parameter.
# if we use .flac the file size is much around 14x smaller than a .wav file. mp3s are not supported through this (to my knowledge)
FluidSynth('soundfonts/Analog Clavinova.sf2').midi_to_audio('fileout.mid','output.wav')

# since I am unsure how the HTML will be implemented, or what the base audio codecs are, we can use .wavs if needed but .flacs will be much smaller

# if they want to hear it, you'll have to open it from the workspace folder. 
# I assume that we would essentially have the file on the server and then have the webpage point to the audio file