from django import forms
from .models import Task

class TaskForm(form.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description', 'important']
      