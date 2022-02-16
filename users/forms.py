from django import forms
from django.utils.translation import gettext as _

class ProfileChangeForm(forms.Form):
    avatar = forms.FileField( required = False, widget = forms.ClearableFileInput())
    first_name = forms.CharField( label = _('First name'), required = False,
        widget = forms.TextInput())
    last_name = forms.CharField( label = _('Last name'), required = False,
        widget = forms.TextInput())
    email = forms.EmailField(label = _('Email'), required = False,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    bio = forms.CharField( label = _('Short bio'), required = False,
        widget = forms.Textarea(attrs={'placeholder': _("Talk about yourself")}) )
