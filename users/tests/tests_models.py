from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from buildings.models import User, Profile, UserMessage

# Create your tests here.
