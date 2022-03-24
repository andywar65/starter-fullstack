from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import Permission

from allauth.account.models import EmailAddress

from users.models import User

@override_settings(USE_I18N=False)#not working
@override_settings(MEDIA_ROOT=Path(settings.MEDIA_ROOT).joinpath('temp'))
class UserViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest user views")
        boss = User.objects.create_superuser('boss', 'boss@example.com',
            'P4s5W0r6')
        EmailAddress.objects.create(user_id=boss.uuid,
            email=boss.email, verified=True, primary=True)

    def test_user_views_status_code_302(self):
        print("\n-Test User Views not logged")
        response = self.client.get(reverse('account_profile'))
        self.assertEqual(response.status_code, 302)
        print("\n--Test Account Profile redirect")
        response = self.client.get(reverse('account_delete'))
        self.assertEqual(response.status_code, 302)
        print("\n--Test Account Delete redirect")
        response = self.client.get(reverse('account_contact'))
        self.assertEqual(response.status_code, 302)
        print("\n--Test Account Contact redirect")

    def test_user_views_status_code_200(self):
        print("\n-Test User Views logged in")
        self.client.login(username='boss', password='P4s5W0r6')
        response = self.client.get(reverse('account_profile'))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Account Profile success")
        response = self.client.get(reverse('account_delete'))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Account Delete success")
        response = self.client.get(reverse('account_contact'))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Account Contact success")
