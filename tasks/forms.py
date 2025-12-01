from django import forms
from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    assignee = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))

    class Meta:
        model = Task
        fields = ['title','description','due_date','status','assignee']