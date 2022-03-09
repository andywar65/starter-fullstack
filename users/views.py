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

class TemplateNamesMixin:
    """Switches template depending on request.htmx"""
    def get_template_names(self):
        if self.request.htmx:
            return [self.template_name.replace('account/', 'account/htmx/')]
        else:
            return [self.template_name]

class TestedPasswordChangeView(ImmutableProfilePassTestMix, TemplateNamesMixin,
    PasswordChangeView):
    pass

class TestedPasswordSetView(ImmutableProfilePassTestMix, PasswordSetView, ):
    pass

class TestedPasswordResetView(ImmutableProfilePassTestMix, TemplateNamesMixin,
    PasswordResetView, ):
    pass

class TestedEmailView(ImmutableProfilePassTestMix, EmailView, ):
    pass

class HTMXLoginView(TemplateNamesMixin, LoginView):
    pass

class HTMXSignupView(TemplateNamesMixin, SignupView):
    pass

class ProfileChangeView(LoginRequiredMixin, ImmutableProfilePassTestMix,
    TemplateNamesMixin, FormView):
    form_class = ProfileChangeForm
    template_name = 'account/account_profile.html'

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
    TemplateNamesMixin, FormView):
    form_class = ProfileDeleteForm
    template_name = 'account/account_delete.html'

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
