from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .utils import *
from .models import *

from django_registration.forms import RegistrationForm

class ChatRegistrationForm(RegistrationForm):

    # Override the __init__ to remove the 'email' field
    def __init__(self, *args, **kwargs):
        super(ChatRegistrationForm, self).__init__(*args, **kwargs)
        
        # This way it worked properly
        self.fields.pop('email')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        username = self.cleaned_data["username"]
        
        if commit:
            user.save()
            ChatUser.objects.create(user=user, username=user.username)

        return user

class EnterChatRoomForm(forms.Form):
    other_user_name = forms.CharField()
    
    def clean(self):
        cd = self.cleaned_data

        other_user_name = cd.get("other_user_name")
        # print('other_user_name', other_user_name)

        if user_exists(other_user_name) == False:
            raise ValidationError("User doesn't exist")

        return cd
