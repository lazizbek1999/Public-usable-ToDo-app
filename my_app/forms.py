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
        