from django import forms
from django.contrib.auth.models import User

from django_registration.forms import RegistrationForm

class ChatRegistrationForm(RegistrationForm):
    # Override the __init__ to remove the 'email' field
    def __init__(self, *args, **kwargs):
        super(ChatRegistrationForm, self).__init__(*args, **kwargs)
        
        # This way it worked properly
        self.fields.pop('email')
    