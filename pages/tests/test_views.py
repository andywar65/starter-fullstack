from django.test import TestCase, override_settings
from django.urls import reverse

from pages.models import HomePage

@override_settings(USE_I18N=False)
class PageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest page views")
        # Set up non-modified objects used by all test methods
        HomePage.objects.create(title='Title')

    def test_homepage_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        print("\n-Test Homepage status 200")
