from django import forms
from .models import Task, Comment


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["due_date"].widget.input_type = "datetime-local"


class TaskFlterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "All"),
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]
    status = forms.ChoiceField(
        choices=STATUS_CHOICES, required=False, label="Status")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'media']
        widgets = {
            "media": forms.FileInput()
        }
