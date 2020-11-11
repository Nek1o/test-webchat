from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import *

from django_registration.backends.one_step.views import RegistrationView

# registration views

class ChatRegistrationView(RegistrationView):
    form_class = ChatRegistrationForm
    success_url = reverse_lazy('index')

# views

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    print(request.user.username)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user': request.user.username
    })
