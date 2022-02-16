from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import User
from .forms import ProfileChangeForm

class ProfileChangeView(LoginRequiredMixin, FormView):
    form_class = ProfileChangeForm
    template_name = 'users/account_profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        if self.user.profile.immutable:
            raise Http404(_("Password cannot be changed by immutable user"))
        super(ProfileChangeView, self).setup(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfileChangeView, self).get_initial()

        initial.update({
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'avatar': self.user.profile.avatar,
            'bio': self.user.profile.bio,
            })
        return initial

    def form_valid(self, form):
        profile = self.user.profile
        self.user.first_name = form.cleaned_data['first_name']
        self.user.last_name = form.cleaned_data['last_name']
        self.user.email = form.cleaned_data['email']
        profile.avatar = form.cleaned_data['avatar']
        profile.bio = form.cleaned_data['bio']
        self.user.save()
        profile.save()
        return super(ProfileChangeView, self).form_valid(form)

    def get_success_url(self):
        return (reverse('account_profile') + '?submitted=True')
