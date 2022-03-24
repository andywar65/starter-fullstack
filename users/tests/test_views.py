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
        User.objects.create_superuser('boss', 'boss@example.com',
            'P4s5W0r6')
        immutable = User.objects.create_user('immutable', 'immu@example.com',
            'P4s5W0r6')
        p = Permission.objects.get(codename='can_not_change_profile')
        immutable.user_permissions.add(p)

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

    def test_immutable_user_views_status_code_403(self):
        print("\n-Test Immutable User Views logged")
        self.client.login(username='immutable', password='P4s5W0r6')
        response = self.client.get(reverse('account_profile'))
        self.assertEqual(response.status_code, 403)
        print("\n--Test Immutable Account Profile forbidden")
        response = self.client.get(reverse('account_delete'))
        self.assertEqual(response.status_code, 403)
        print("\n--Test Immutable Account Delete forbidden")
        response = self.client.get(reverse('account_contact'))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Immutable Account Contact success")

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
