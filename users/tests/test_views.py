from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import Permission

from allauth.account.models import EmailAddress

from users.models import User


@override_settings(USE_I18N=False)
@override_settings(MEDIA_ROOT=Path(settings.MEDIA_ROOT).joinpath("temp"))
class UserViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest user views")
        boss = User.objects.create_superuser("boss", "boss@example.com", "P4s5W0r6")
        EmailAddress.objects.create(user_id=boss.uuid)
        immutable = User.objects.create_user(
            "immutable", "immu@example.com", "P4s5W0r6"
        )
        p = Permission.objects.get(codename="can_not_change_profile")
        immutable.user_permissions.add(p)

    def tearDown(self):
        """Checks existing files, then removes them"""
        path = Path(settings.MEDIA_ROOT).joinpath("uploads/images/users/")
        list = [e for e in path.iterdir() if e.is_file()]
        for file in list:
            Path(file).unlink()

    def test_user_views_status_code_302(self):
        print("\n-Test User Views not logged")

        response = self.client.get(reverse("account_profile"))
        self.assertRedirects(
            response,
            reverse("account_login") + "?next=/accounts/profile/",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Account Profile redirect")

        response = self.client.get(reverse("account_delete"))
        self.assertRedirects(
            response,
            reverse("account_login") + "?next=/accounts/profile/delete/",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Account Delete redirect")

        response = self.client.get(reverse("account_contact"))
        self.assertRedirects(
            response,
            reverse("account_login") + "?next=/accounts/contact/",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Account Contact redirect")

    def test_immutable_user_views_status_code_403(self):
        print("\n-Test Immutable User Views logged")
        self.client.login(username="immutable", password="P4s5W0r6")

        response = self.client.get(reverse("account_profile"))
        self.assertEqual(response.status_code, 403)
        print("\n--Test Immutable Account Profile forbidden")

        response = self.client.get(reverse("account_delete"))
        self.assertEqual(response.status_code, 403)
        print("\n--Test Immutable Account Delete forbidden")

        response = self.client.get(reverse("account_contact"))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Immutable Account Contact success")

    def test_user_views_status_code_200(self):
        print("\n-Test User Views logged in")
        self.client.login(username="boss", password="P4s5W0r6")

        response = self.client.get(reverse("account_profile"))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Account Profile success")

        response = self.client.get(reverse("account_delete"))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Account Delete success")

        response = self.client.get(reverse("account_contact"))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Account Contact success")

    def test_change_account_profile(self):
        print("\n-Test Change account profile")
        self.client.login(username="boss", password="P4s5W0r6")
        img_path = Path(settings.STATIC_ROOT).joinpath("tests/image.jpg")
        with open(img_path, "rb") as f:
            content = f.read()

        response = self.client.post(
            reverse("account_profile"),
            {
                "first_name": "",
                "last_name": "",
                "email": "boss@example.com",
                "avatar": SimpleUploadedFile("image.jpg", content, "image/jpg"),
                "bio": "",
            },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("account_profile") + "?submitted=True",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Add Avatar redirect")

        response = self.client.post(
            reverse("account_profile"),
            {
                "first_name": "",
                "last_name": "",
                "email": "boss@example.com",
                "avatar": "",
                "del_avatar": True,
                "bio": "",
            },
            headers={"HX-REQUEST": True},  # not working
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("account_profile") + "?submitted=True",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Delete Avatar redirect")

    def test_send_account_contact(self):
        print("\n-Test send account contact")
        self.client.login(username="boss", password="P4s5W0r6")

        response = self.client.post(
            reverse("account_contact"),
            {"subject": "Subject", "body": "Message"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("account_contact") + "?submitted=True",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test send account contact redirect")

    def test_delete_account_profile(self):
        print("\n-Test delete account profile")
        self.client.login(username="boss", password="P4s5W0r6")

        response = self.client.post(
            reverse("account_delete"), {"delete": True}, follow=True
        )
        self.assertRedirects(
            response, reverse("home"), status_code=302, target_status_code=404
        )  # we don't have HomePage
        print("\n--Test delete account profile redirect")
