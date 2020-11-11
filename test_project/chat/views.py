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
        print(request.POST)
        form = EnterChatRoomForm(data=request.POST)

        if form.is_valid():
            new_chat_session = get_or_create_chat_session_synch(request.user.username, form.data['other_user_name']) # form.other_user_name ???

            print(new_chat_session.id)

            return redirect('/chat/' + str(new_chat_session.id) + '/') # ???
        
        print('enter form isnt valid')
        context = { 'form': form, 'errors': form.errors } # ???
        return render(request, 'chat/index.html', context)

# room_id == ChatSession.id

def room(request, room_id):
    user = User.objects.get(username=request.user.username)
    session = ChatSession.objects.get(id=int(room_id))
    print(session.users)

    # if session:
        # raise PermissionDenied

    return render(request, 'chat/room.html', {
        'room_id': room_id,
        'user': request.user.username
    })
