from django.shortcuts import render
from django.urls import reverse_lazy

# registration views

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    print(request.user.username)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user': request.user.username
    })
