from django.http import HttpResponse
from django.http import JsonResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import midiAngeloConversions
from . import midi_to_audio_conversion


def home(request):
	return render(request, 'midiCanvas.html')

@csrf_exempt
def image(request):
	midi_string = request.body.decode("utf-8")
	midi_file = midiAngeloConversions.canvas2midi('output_midi', midi_string)
	audio_file = midi_to_audio_conversion.createWav(midi_file, 'Choir Aahs.sf2', 'output_audio')
	return JsonResponse({'code': 200, 'payload': audio_file})


def login(request):
	return render(request, 'login.html')

def signup(request):
	return render(request, 'login.html')	