from django.http import HttpResponse
from django.shortcuts import render
from . import midiAngeloConversions
from . import midiConverter

def canvas(request, user_id=0):
	html = "<html><body>This is our canvas page.</body></html>"
	return HttpResponse(html)

def user_feed(request, user_id=0):
	return render(request, 'user/user.html', {'user_id': user_id})

def canvas_view(request, canvas_id=0):
	print("We are ready to return HTML")
	return render(request, "canvas.html")

def create_mp3(request):
	print(request)
	new_mp3 = open("/pretty_boy.mp3", "rb").read()
	return HttpResponse(new_mp3, headers={
		'Content-Type': 'application/mp3',
		'Content-Disposition': 'attachment; filename="new_mozart.mp3"'
	})