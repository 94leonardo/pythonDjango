from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def HelloWord(request):
    title = 'Hello Word'
    return render(request, 'signup.html', {
        'form': UserCreationForm
    })
