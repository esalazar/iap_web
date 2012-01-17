from django.http import HttpResponse

def index(request):
    return HttpResponse("EdEx")

def lecture(request):
    return HttpResponse("Lecture")

def search(request):
    return HttpResponse("Search")

def notes(request):
    return HttpResponse("Notes")

def profile(request):
    return HttpResponse("profile")
