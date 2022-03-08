import os
from django.http import HttpResponse
from django.http import JsonResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import midiAngeloConversions
from . import midi_to_audio_conversion
from django.conf import settings
import base64

def home(request):
	return render(request, 'midiCanvas.html')

@csrf_exempt
def image(request):
	midi_string = request.body.decode("utf-8") #request.body.image_string
	sound = "Harp" #request.body.sound
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

def signup(request):
	return render(request, 'login.html')	