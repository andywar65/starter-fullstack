from django.test import TestCase, override_settings

from pages.models import HomePage

@override_settings(USE_I18N=False)
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest page models")
        # Set up non-modified objects used by all test methods
        HomePage.objects.create(title='Title')
        HomePage.objects.create(intro='No title')

    def test_homepage_str(self):
        hp1 = HomePage.objects.get(title='Title')
        self.assertEquals(hp1.__str__(), 'Title')
        hp2 = HomePage.objects.get(intro='No title')
        self.assertEquals(hp2.__str__(), 'Home Page - '+str(hp2.id))
