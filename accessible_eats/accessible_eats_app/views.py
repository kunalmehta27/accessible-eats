from django.shortcuts import render
from .helpers import text_to_object

# Create your views here.
def index(request):
	text_to_object('Leals 79124')
	return render(request, "index.html", {})


def review(request):
	if request.POST:
		print request.POST
		return render(request, "thanks.html", {})
	else:	
		return render(request, "review.html", {})


def search(request):
	return render(request, "search.html", {})