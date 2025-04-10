from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def HelloWord(request):
    return HttpResponse("Hello World")
