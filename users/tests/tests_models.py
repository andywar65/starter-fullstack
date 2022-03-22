from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User, Profile, UserMessage

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='andy.war65', password='P4s5W0r6',
            first_name='Andrea', last_name='Guerra', email='andy@war.com')
        #next save is just for coverage purposes
        user.save()
        profile = user.profile
        profile.bio = 'My biography'
        profile.save()

    def test_profile_get_full_name(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.profile.get_full_name(), 'Andrea Guerra')
