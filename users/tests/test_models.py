from pathlib import Path

from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from project.utils import check_wide_image
from users.models import User, UserMessage


@override_settings(USE_I18N=False)
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest user models")
        # Set up non-modified objects used by all test methods
        user = User.objects.create(
            username="andy.war65",
            password="P4s5W0r6",
            first_name="Andrea",
            last_name="Guerra",
            email="andy@war.com",
        )
        # next save is just for coverage purposes
        user.save()
        SocialAccount.objects.create(
            user_id=user.uuid, provider="google", extra_data={"picture": "foo"}
        )
        profile = user.profile
        profile.bio = "My biography"
        profile.save()
        User.objects.create(
            username="nonames", password="P4s5W0r6", email="nonames@war.com"
        )
        UserMessage.objects.create(user_id=user.uuid, subject="Foo", body="Bar")

    def test_user_get_avatar(self):
        user = User.objects.get(username="andy.war65")
        self.assertEquals(user.get_avatar(), "foo")
        print("\n-Tested User get avatar")

    def test_profile_get_names(self):
        user = User.objects.get(username="andy.war65")
        self.assertEquals(user.profile.__str__(), "andy.war65")
        print("\n-Tested Profile __str__")
        self.assertEquals(user.__str__(), "andy.war65")
        print("\n-Tested User __str__")
        self.assertEquals(user.get_full_name(), "Andrea Guerra")
        print("\n-Tested User full name")
        self.assertEquals(user.get_short_name(), "Andrea")
        print("\n-Tested User short name")

    def test_profile_get_no_names(self):
        user = User.objects.get(username="nonames")
        self.assertEquals(user.profile.__str__(), "nonames")
        print("\n-Tested Profile no __str__")
        self.assertEquals(user.__str__(), "nonames")
        print("\n-Tested User no __str__")
        self.assertEquals(user.get_full_name(), "nonames")
        print("\n-Tested User no full name")
        self.assertEquals(user.get_short_name(), "nonames")
        print("\n-Tested User no short name")

    def test_usermessage_get_str(self):
        message = UserMessage.objects.get(subject="Foo")
        self.assertEquals(message.__str__(), "Message - " + str(message.id))
        print("\n-Tested UserMessage __str__")


@override_settings(MEDIA_ROOT=Path(settings.MEDIA_ROOT).joinpath("temp"))
class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest profile models")
        # Set up non-modified objects used by all test methods
        user = User.objects.create(
            username="raw.ydna56", password="P4s5W0r6", email="ydna@raw.com"
        )
        profile = user.profile
        img_path = Path(settings.STATIC_ROOT).joinpath("tests/image.jpg")
        with open(img_path, "rb") as f:
            content = f.read()
        profile.temp_image = SimpleUploadedFile("image.jpg", content, "image/jpg")
        profile.save()

    def tearDown(self):
        """Checks existing files, then removes them"""
        path = Path(settings.MEDIA_ROOT).joinpath("uploads/images/users/")
        list = [e for e in path.iterdir() if e.is_file()]
        for file in list:
            Path(file).unlink()
        path = Path(settings.MEDIA_ROOT).joinpath("_versions/images/users/")
        list = [e for e in path.iterdir() if e.is_file()]
        for file in list:
            Path(file).unlink()

    def test_profile_fb_image(self):
        user = User.objects.get(username="raw.ydna56")
        self.assertEquals(user.profile.temp_image, "")
        print("\n-Tested Profile temp_image")
        self.assertEquals(user.profile.fb_image.path, "uploads/images/users/image.jpg")
        print("\n-Tested Profile fb_image")

    def test_check_wide_image(self):
        user = User.objects.get(username="raw.ydna56")
        check_wide_image(user.profile.fb_image)
        path = Path(settings.MEDIA_ROOT).joinpath(
            "_versions/images/users/image_wide.jpg"
        )
        img = Image.open(path)
        self.assertEquals(img.width, 1600)
        print("\n-Tested check wide image utility")
