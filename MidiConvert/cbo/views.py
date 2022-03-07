from django.http import HttpResponse
from django.http import JsonResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def home(request):
	print("test home")
	return render(request, 'midiCanvas.html')

@csrf_exempt
def image(request):
	print(request.body)
	midi_string = request.body.decode("utf-8")
	print(midi_string)
	return JsonResponse({'code': 200, 'payload': midi_string})


def login(request):
	return render(request, 'login.html')

def signup(request):
	return render(request, 'login.html')	