from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views import View

from django_registration.backends.one_step.views import RegistrationView

from .forms import *
from .utils import *

# registration views

class ChatRegistrationView(RegistrationView):
    form_class = ChatRegistrationForm
    success_url = reverse_lazy('index')

# views

class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = EnterChatRoomForm()
        context = { 'form': form }

        return render(request, 'chat/index.html', context)

    def post(self, request, *args, **kwargs):
        form = EnterChatRoomForm(data=request.POST)

        if form.is_valid() and form.data['other_user_name'] != request.user.username:
            new_chat_session = get_or_create_chat_session(request.user.username, form.data['other_user_name'])

            return redirect('/chat/' + str(new_chat_session.id) + '/') 
        
        if form.data['other_user_name'] != request.user.username:
            error = "You can't chat with yourself"
            context = { 'form': form, 'error': error } 
            return render(request, 'chat/index.html', context)
        else:
            error = "There is no user named " + form.data['other_user_name']
            context = { 'form': form, 'error': error } 
            return render(request, 'chat/index.html', context)

# room_id == ChatSession.id

def room(request, room_id):
    user = User.objects.get(username=request.user.username)
    session = ChatSession.objects.get(id=int(room_id))

    if user not in session.users.all():
        raise PermissionDenied

    return render(request, 'chat/room.html', {
        'room_id': room_id,
        'user': request.user.username
    })
