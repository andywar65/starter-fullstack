from django.test import TestCase, override_settings
from django.urls import reverse

from pages.models import Article, HomePage


@override_settings(USE_I18N=False)
class PageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest page views")
        # Set up non-modified objects used by all test methods
        HomePage.objects.create(title="Title")
        Article.objects.create(title="First", date="2022-04-09")

    def test_homepage_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        print("\n-Test Homepage status 200")
        self.assertTemplateUsed(response, "pages/home.html")
        print("\n-Test Homepage template")

    def test_no_homepage(self):
        HomePage.objects.all().delete()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 404)
        print("\n-Test Homepage status 404")

    def test_article_template(self):
        response = self.client.get(
            reverse(
                "pages:article_detail",
                kwargs={"year": 2022, "month": 4, "day": 9, "slug": "first"},
            )
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test Article status 200")
        self.assertTemplateUsed(response, "pages/article_detail.html")
        print("\n-Test Article template")
