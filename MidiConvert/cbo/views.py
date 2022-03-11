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

#Render the landing page
def home(request):
	return render(request, 'index.html')

#Render the admin testing page
def test(request):
	return render(request, "test.html")

#Convert an image in the request
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

#Render the login page
def login(request):
	return render(request, 'login.html')

#Render the drawing canvas page
def canvas(request):
	return render(request, 'midiCanvas.html')

#Render the user signup page
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

#Input: a list of strings with no file extensions
#Return: a list of strings that relate to the filepaths
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
	# TEST SECTION 1: createWav
	# Test 1
	if midi_to_audio_conversion.createWav('filein.midd', '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wav') == -1:
		test_results['pass'].append("Test 1: midi input extension detection pass")
	else:
		test_results['fail'].append("Test 1: Error in midi input extension detection")

	# Test 2
	if midi_to_audio_conversion.createWav('filein.mid', '/app/cbo/soundfonts/Early Ens.sf3', 'melody.wav') == -1:
		test_results['pass'].append("Test 2: soundfont input extension detection pass")
	else:
		test_results['fail'].append("Test 2: Error in soundfont input extension detection")

	# Test 3
	if midi_to_audio_conversion.createWav('filein.mid', '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wave') == -1:
		test_results['pass'].append("Test 3: wav output extension detection pass")
	else:
		test_results['fail'].append("Test 3: Error in wav output extension detection")

	# Test 4
	if midi_to_audio_conversion.createWav('filein.mid', '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wav',20) == 1:
		test_results['pass'].append("Test 4: decibel conversion output - positive value pass")
	else:
		test_results['fail'].append("Test 4: Error decibel conversion output - not turning up volume")

	# Test 5
	if midi_to_audio_conversion.createWav('filein.mid', '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wav',-20) == 2:
		test_results['pass'].append("Test 5: decibel conversion output - negative value pass")
	else:
		test_results['fail'].append("Test 5: Error decibel conversion output - not turning down volume")

	# Test 6
	if midi_to_audio_conversion.createWav('filein.mid', '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wav') == 3:
		test_results['pass'].append("Test 6: basic conversion - no decibel alteration pass")
	else:
		test_results['fail'].append("Test 6: Error in basic conversion - no decibel alteration")

	# TEST SECTION 2: OVERLAYWAV
	sound_list = ['/app/cbo/soundfonts/Early Ens.sf2', '/app/cbo/soundfonts/Piano.sf2', '/app/cbo/soundfonts/Sax Section.sf2', '/app/cbo/soundfonts/Celesta.sf2']
	bad_sound_list = ['/app/cbo/soundfonts/Early Ens.sf2', '/app/cbo/soundfonts/Piano.sf3', '/app/cbo/soundfonts/Sax Section.sf2', '/app/cbo/soundfonts/Celesta.sf2']
	
	# Test 7
	if midi_to_audio_conversion.overlayWavs(sound_list, '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wav') == 0:
		test_results['pass'].append("Test 7: basic conversion - overlayWav works - no added Db")
	else:
		test_results['fail'].append("Test 7: Error in basic conversion - overlayWav does not work - no added db - perhaps file path error?")

	# Test 8
	if midi_to_audio_conversion.overlayWavs(sound_list, '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wav', 10) == 0:
		test_results['pass'].append("Test 7: basic conversion - overlayWav works - higher Db")
	else:
		test_results['fail'].append("Test 7: Error in basic conversion - overlayWav does not work - higher db - perhaps file path error?")

	# Test 9
	if midi_to_audio_conversion.overlayWavs(sound_list, '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wav', -10) == 0:
		test_results['pass'].append("Test 7: basic conversion - overlayWav works - lowered Db")
	else:
		test_results['fail'].append(
			"Test 7: Error in basic conversion - overlayWav does not work - lowered db - perhaps file path error?")

	# Test 10
	if midi_to_audio_conversion.overlayWavs(bad_sound_list, '/app/cbo/soundfonts/Early Ens.sf2', 'melody.wav') == -1:
		test_results['pass'].append("Test 7: basic conversion - overlayWav has correctly identified an error in the soundlist - no added Db")
	else:
		test_results['fail'].append("Test 7: Error in basic conversion - overlayWav does not recognize bad file - no added db - perhaps file path error?")

	#Test getSoundFonts(tester):	

	return HttpResponse(json.dumps(test_results), content_type='application/json')
