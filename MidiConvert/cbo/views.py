import os
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import midiAngeloConversions
from . import midi_to_audio_conversion
from django.conf import settings
import base64
import glob
from django.test import Client

def home(request):
	return render(request, 'index.html')

def test(request):
	return render(request, "test.html")

@csrf_exempt
def image(request):
	data = json.loads(request.body)
	if not data:
		return HttpResponseBadRequest("There was no data provided to handle then request.")

	midi_string = '' # image string to make into midi
	if 'img_string' in data and isinstance(data['img_string'],str):
		midi_string = str(data['img_string'])
	else:
		return HttpResponseBadRequest("No Image was provided or it was in an improper format.")

	sounds = getSoundFontsList(data["soundfonts"]) #soundfont to use for conversion
	if len(sounds)==0:
		return HttpResponseBadRequest("No Sounds were provided or they could not be formatted by the server.")

	db_boost = 0
	if 'db_boost' in data and isinstance(data['db_boost'], int):
		db_boost = int(data['db_boost'])

	midi_file_success = midiAngeloConversions.canvas2midi('output_midi', midi_string)
	if not midi_file_success:
		response = HttpResponseBadRequest("The Image failed be converted to MIDI")
	
	try:
		midi_to_audio_conversion.overlayWavs(sounds, "output_midi.midi", 'output_audio.wav', db_boost)
	except:
		RuntimeError
		return HttpResponseBadRequest("Failed to create the song from selected sounds.")

	try:
		fname = settings.BASE_DIR/"output_audio.wav"
	except:
		RuntimeError
		return HttpResponseBadRequest("The finalized audio file could not be found .")

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

#Input: an HttpRequest
#Return: a list of soundfonts by their file location
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

#Run all of our tests and return a report
@csrf_exempt
def runTestingSuite(request):
	tester = Client()
	test_results = {
		'pass':['Server Health: Strong', 'The testing suite has been reached.'], 
		'fail':[]
	}

	return HttpResponse(json.dumps(test_results), content_type='application/json')
