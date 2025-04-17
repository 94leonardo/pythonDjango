from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here. ruta de las vistas

def home(request):
   
    return render(request, 'home.html')
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm              
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #registro user
            try:
                user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'])

                user.save()
                return HttpResponse('User create susserfully')
            except:
                
                return HttpResponse('User alredy exist')

            
        return HttpResponse('Password do not match')
    
    
