from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _

from allauth.account.models import EmailAddress
from allauth.account.views import (PasswordChangeView, PasswordSetView,
    PasswordResetView, EmailView, LoginView, SignupView)

from .models import User
from .forms import *

class ImmutableProfilePassTestMix(UserPassesTestMixin):
    """Controls if user has immutable profile. If true, test is not passed."""
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return not self.request.user.has_perm('users.can_not_change_profile')

class TestedPasswordChangeView(ImmutableProfilePassTestMix, PasswordChangeView):

    def get_template_names(self):
        if self.request.htmx:
            return ['account/password_change_htmx.html']
        else:
            return ['account/password_change.html']

class TestedPasswordSetView(ImmutableProfilePassTestMix, PasswordSetView, ):
    pass

class TestedPasswordResetView(ImmutableProfilePassTestMix, PasswordResetView, ):

    def get_template_names(self):
        if self.request.htmx:
            return ['account/password_reset_htmx.html']
        else:
            return ['account/password_reset.html']

class TestedEmailView(ImmutableProfilePassTestMix, EmailView, ):
    pass

class HTMXLoginView(LoginView):

    def get_template_names(self):
        if self.request.htmx:
            return ['account/login_htmx.html']
        else:
            return ['account/login.html']

class HTMXSignupView(SignupView):

    def get_template_names(self):
        if self.request.htmx:
            return ['account/signup_htmx.html']
        else:
            return ['account/signup.html']

class ProfileChangeView(LoginRequiredMixin, ImmutableProfilePassTestMix,
    FormView):
    form_class = ProfileChangeForm

    def get_template_names(self):
        if self.request.htmx:
            return ['account/account_profile_htmx.html']
        else:
            return ['account/account_profile.html']

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super(ProfileChangeView, self).setup(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfileChangeView, self).get_initial()

        initial.update({
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'avatar': self.user.profile.avatar.original,
            'bio': self.user.profile.bio,
            })
        return initial

    def form_valid(self, form):
        #assign user form fields
        self.user.first_name = form.cleaned_data['first_name']
        self.user.last_name = form.cleaned_data['last_name']
        self.user.email = form.cleaned_data['email']
        self.user.save()
        #assign profile form fields
        profile = self.user.profile
        profile.bio = form.cleaned_data['bio']
        profile.save()
        #assign avatar form field
        avatar = self.user.profile.avatar
        avatar.original = form.cleaned_data['avatar']
        avatar.save()
        return super(ProfileChangeView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'submitted' in self.request.GET:
            context['submitted'] = self.request.GET['submitted']
        return context

    def get_success_url(self):
        return (reverse('account_profile') + '?submitted=True')

class ProfileDeleteView(LoginRequiredMixin, ImmutableProfilePassTestMix,
    FormView):
    form_class = ProfileDeleteForm

    def get_template_names(self):
        if self.request.htmx:
            return ['account/account_delete_htmx.html']
        else:
            return ['account/account_delete.html']

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super(ProfileDeleteView, self).setup(request, *args, **kwargs)

    def form_valid(self, form):
        self.user.is_active = False
        self.user.first_name = ''
        self.user.last_name = ''
        self.user.email = ''
        self.user.save()
        profile = self.user.profile
        avatar = profile.avatar
        profile.delete()
        avatar.delete()
        EmailAddress.objects.filter(user_id=self.user.uuid).delete()
        return super(ProfileDeleteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home')
