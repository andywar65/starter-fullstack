from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from .models import Story


class ShotgunCreateForm(forms.Form):
    title = forms.CharField(label=_("Title"), required=True, widget=forms.TextInput())
    body = forms.CharField(label=_("Text"), required=True, widget=TinyMCE())
    image = forms.FileField(required=True, widget=forms.FileInput())
    description = forms.CharField(
        label=_("Image caption"), required=False, widget=forms.TextInput()
    )


class StorySelectForm(forms.Form):
    # This form is never used in the project,
    # but is here to show how to use action_with_form in the admin
    story = forms.ModelChoiceField(
        queryset=Story.objects.all(),
        label=_("Select Story"),
        required=True,
        widget=forms.Select(),
    )
