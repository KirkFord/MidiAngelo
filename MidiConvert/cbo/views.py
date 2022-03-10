import os
from django.http import HttpResponse, HttpResponseBadRequest
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import midiAngeloConversions
from . import midi_to_audio_conversion
from django.conf import settings
import base64
import glob

def home(request):
	return render(request, 'index.html')

@csrf_exempt
def image(request):
	data = json.loads(request.body)
	midi_string = data['img_string'] # image string to make into midi
	sounds = getSoundFontsList(data["soundfonts"]) #soundfont to use for conversion
	db_boost = 0
	if 'db_boost' in data and type(data['db_boost']) == 'int':
		db_boost = int(data['db_boost'])
	midi_file_success = midiAngeloConversions.canvas2midi('output_midi', midi_string)
	if not midi_file_success:
		response = HttpResponseBadRequest("The Image could not be converted to MIDI")
	midi_to_audio_conversion.overlayWavs(sounds, "output_midi.midi", 'output_audio.wav', db_boost)

	fname = settings.BASE_DIR/"output_audio.wav"
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
	return HttpResponse(json.dumps(soundfont_names), content_type='application/json')

def getSoundFontsList(soundfonts):
	formatted_soundfonts = []
	for i in range(len(soundfonts)):
		formatted_soundfonts.append("/app/cbo/soundfonts/"+soundfonts[i]+".sf2")
	
	return formatted_soundfonts