from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','descr','image','is_completed']
        # widgets = {
        #     'is_completed': forms.HiddenInput()
        # }
        
        
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prevents browsers from auto-saving or prompting on faulty password configurations
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password'})

