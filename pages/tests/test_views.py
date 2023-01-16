from django.contrib.flatpages.models import FlatPage
from django.test import TestCase, override_settings
from django.urls import reverse

from pages.models import Article, HomePage
from users.models import User


@override_settings(USE_I18N=False)
class PageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest page views")
        # Set up non-modified objects used by all test methods
        User.objects.create_superuser("boss", "boss@example.com", "P4s5W0r6")
        HomePage.objects.create(title="Title")
        Article.objects.create(id=1, title="First", date="2022-04-09")
        FlatPage.objects.create(id=1, title="Flatpage", content="Foo")

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
                kwargs={"year": 2022, "month": 4, "day": 9, "slug": "first-1"},
            )
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test Article status 200")
        self.assertTemplateUsed(response, "pages/article_detail.html")
        print("\n-Test Article template")

    def test_flat_page_admin(self):
        # just for coverage
        self.client.login(username="boss", password="P4s5W0r6")
        response = self.client.get("/admin/flatpages/flatpage/1/change/")
        self.assertEqual(response.status_code, 200)
        print("\n-Test Flatpage admin")
