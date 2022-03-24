from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import UserMessage

class ProfileChangeForm(forms.Form):
    avatar = forms.FileField( required = False, widget = forms.FileInput())
    first_name = forms.CharField( label = _('First name'), required = False,
        widget = forms.TextInput())
    last_name = forms.CharField( label = _('Last name'), required = False,
        widget = forms.TextInput())
    email = forms.EmailField(label = _('Email'), required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    bio = forms.CharField( label = _('Short bio'), required = False,
        widget = forms.Textarea(attrs={'placeholder': _("Talk about yourself")}) )

class ProfileChangeDelAvatarForm(forms.Form):
    del_avatar = forms.BooleanField( label=_("Check to delete Avatar"),
        required = False,)
    avatar = forms.FileField( label = _('Change Avatar'), required = False, 
        widget = forms.FileInput())
    first_name = forms.CharField( label = _('First name'), required = False,
        widget = forms.TextInput())
    last_name = forms.CharField( label = _('Last name'), required = False,
        widget = forms.TextInput())
    email = forms.EmailField(label = _('Email'), required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    bio = forms.CharField( label = _('Short bio'), required = False,
        widget = forms.Textarea(attrs={'placeholder': _("Talk about yourself")}) )

class ProfileDeleteForm(forms.Form):
    delete = forms.BooleanField( label=_("Check and Confirm to delete* the profile"),
        required = True,)

class ContactForm(ModelForm):

    class Meta:
        model = UserMessage
        fields = ('subject', 'body', )
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': _("Write here the subject")}),
            'body': forms.Textarea(attrs={'placeholder': _("Write here the message")}),
            }
