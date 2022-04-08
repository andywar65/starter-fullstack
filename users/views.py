from allauth.account.models import EmailAddress
from allauth.account.views import (
    EmailView,
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordSetView,
    SignupView,
)
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView

from .forms import (
    ContactForm,
    ProfileChangeDelAvatarForm,
    ProfileChangeForm,
    ProfileDeleteForm,
)
from .models import UserMessage


class HxTemplateMixin:
    """Switches template depending on request.htmx"""

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        else:
            return [self.template_name]


class TestedPasswordChangeView(
    PermissionRequiredMixin, HxTemplateMixin, PasswordChangeView
):
    template_name = "account/htmx/password_change.html"
    permission_required = "users.change_profile"


class TestedPasswordSetView(
    PermissionRequiredMixin,
    PasswordSetView,
):
    template_name = "account/htmx/password_set.html"
    permission_required = "users.change_profile"


class TestedPasswordResetView(
    PermissionRequiredMixin,
    HxTemplateMixin,
    PasswordResetView,
):
    template_name = "account/htmx/password_reset.html"
    permission_required = "users.change_profile"


class TestedEmailView(
    PermissionRequiredMixin,
    EmailView,
):
    template_name = "account/htmx/email.html"
    permission_required = "users.change_profile"


class HTMXLoginView(HxTemplateMixin, LoginView):
    template_name = "account/htmx/login.html"


class HTMXLogoutView(HxTemplateMixin, LogoutView):
    template_name = "account/htmx/logout.html"


class HTMXSignupView(HxTemplateMixin, SignupView):
    template_name = "account/htmx/signup.html"


class ProfileChangeView(
    LoginRequiredMixin, PermissionRequiredMixin, HxTemplateMixin, FormView
):
    form_class = ProfileChangeForm
    template_name = "account/htmx/account_profile.html"
    permission_required = "users.change_profile"

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super(ProfileChangeView, self).setup(request, *args, **kwargs)

    def get_form_class(self):
        if self.user.profile.fb_image:
            self.form_class = ProfileChangeDelAvatarForm
        return self.form_class

    def get_initial(self):
        initial = super(ProfileChangeView, self).get_initial()

        initial.update(
            {
                "del_avatar": False,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
                "bio": self.user.profile.bio,
            }
        )
        return initial

    def form_valid(self, form):
        # assign user form fields
        self.user.first_name = form.cleaned_data["first_name"]
        self.user.last_name = form.cleaned_data["last_name"]
        self.user.email = form.cleaned_data["email"]
        self.user.save()
        # assign profile form fields
        profile = self.user.profile
        profile.bio = form.cleaned_data["bio"]
        profile.temp_image = form.cleaned_data["avatar"]
        if "del_avatar" in form.cleaned_data and form.cleaned_data["del_avatar"]:
            profile.fb_image = None
        profile.save()

        return super(ProfileChangeView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "submitted" in self.request.GET:
            context["submitted"] = self.request.GET["submitted"]
        return context

    def get_success_url(self):
        return reverse("account_profile") + "?submitted=True"


class ProfileDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, HxTemplateMixin, FormView
):
    form_class = ProfileDeleteForm
    template_name = "account/htmx/account_delete.html"
    permission_required = "users.change_profile"

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super(ProfileDeleteView, self).setup(request, *args, **kwargs)

    def form_valid(self, form):
        self.user.is_active = False
        self.user.first_name = ""
        self.user.last_name = ""
        self.user.email = ""
        self.user.save()
        profile = self.user.profile
        profile.delete()
        EmailAddress.objects.filter(user_id=self.user.uuid).delete()
        SocialAccount.objects.filter(user_id=self.user.uuid).delete()
        return super(ProfileDeleteView, self).form_valid(form)

    def get_success_url(self):
        return reverse("home")


class ContactFormView(
    LoginRequiredMixin, PermissionRequiredMixin, HxTemplateMixin, FormView
):
    form_class = ContactForm
    template_name = "account/htmx/contact.html"
    permission_required = "users.change_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "submitted" in self.request.GET:
            context["submitted"] = True
        return context

    def form_valid(self, form):
        subject = form.cleaned_data["subject"]
        body = form.cleaned_data["body"]
        user = self.request.user
        UserMessage.objects.create(user_id=user.uuid, subject=subject, body=body)
        recipient = settings.EMAIL_RECIPIENT
        msg = "%(body)s\n\n%(from)s: %(full)s (%(email)s)" % {
            "body": body,
            "from": _("From"),
            "full": user.get_full_name(),
            "email": user.email,
        }
        mailto = [
            recipient,
        ]
        email = EmailMessage(subject, msg, settings.SERVER_EMAIL, mailto)
        email.send()
        return super(ContactFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("account_contact") + "?submitted=True"
