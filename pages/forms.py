from django import forms
from django.utils.translation import gettext_lazy as _


class ShotgunCreateForm(forms.Form):
    title = forms.CharField(label=_("Title"), required=True, widget=forms.TextInput())
    body = forms.CharField(label=_("Text"), required=True, widget=forms.Textarea())
    image = forms.FileField(required=True, widget=forms.FileInput())
    description = forms.CharField(
        label=_("Image caption"), required=False, widget=forms.TextInput()
    )
