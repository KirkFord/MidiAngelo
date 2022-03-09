import os
from django.http import HttpResponse
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import midiAngeloConversions
from . import midi_to_audio_conversion
from django.conf import settings
import base64
import glob

def home(request):
	print("test home")
	return render(request, 'index.html')

@csrf_exempt
def image(request):
	data = json.loads(request.body)
	midi_string = data['img_string'] # image string to make into midi
	sound = data["soundfont"] #soundfont to use for conversion
	sound_path = "cbo/soundfonts/"+sound+".sf2"
	midi_file = midiAngeloConversions.canvas2midi('output_midi', midi_string)
	audio_file = midi_to_audio_conversion.createWav("output_midi.midi", settings.BASE_DIR/sound_path, 'output_audio.flac')
	fname = settings.BASE_DIR/"output_audio.flac"
	with open(fname,"rb") as f: audio_encoded = base64.b64encode(f.read())
	#convert audio file to JSON
	response = HttpResponse(audio_encoded, content_type='application/json')
	return response

def login(request):
	return render(request, 'login.html')

def canvas(request):
	return render(request, 'midiCanvas.html')

def signup(request):
	return render(request, 'login.html')	

def getSoundFonts(request):

	soundfont_names = []
	soundfont_names = glob.glob("/app/cbo/soundfonts/*.sf2")
	for s in range(len(soundfont_names)):
		soundfont_names[s] = soundfont_names[s][20:-4]
		print(soundfont_names[s])
	print(soundfont_names)
	return HttpResponse(json.dumps(soundfont_names), content_type='application/json')
