from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from pages.models import Article

from .utils import generate_unique_slug


class PendingMigrationsTests(TestCase):
    """Copy/paste from 'Boost your Django DX', by Adam Johnson"""

    def test_no_pending_migrations(self):
        print("\nTest pending migrations")
        out = StringIO()
        try:
            call_command(
                "makemigrations",
                "--dry-run",
                "--check",
                stdout=out,
                stderr=StringIO(),
            )
        except SystemExit:  # pragma: no cover
            raise AssertionError("Pending migrations:\n" + out.getvalue()) from None


@override_settings(USE_I18N=False)
class ProjectViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest project views")
        # Set up non-modified objects used by all test methods

    def test_select_language_view(self):
        response = self.client.get(reverse("select_language"))
        self.assertEqual(response.status_code, 200)
        print("\n-Test select language status 200")

        self.assertTemplateUsed(response, "language_selector.html")
        print("\n-Test select language template")


@override_settings(USE_I18N=False)
class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest search views")
        Article.objects.create(
            id=1,
            title="Article 4",
            date="2020-05-10",
            body="Foo",
        )

    def test_search_results_view_status_code(self):
        response = self.client.get(reverse("search_results") + "?q=foo")
        self.assertEqual(response.status_code, 200)
        print("\n-Test search status 200")

        self.assertTemplateUsed(response, "search_results.html")
        print("\n-Test search template")

        self.assertTrue(response.context["success"])
        print("\n-Test search success")

        response = self.client.get(reverse("search_results") + "?q=")
        self.assertFalse(response.context["success"])
        print("\n-Test search not validating")

        response = self.client.get(reverse("search_results") + "?q=false")
        self.assertFalse(response.context["success"])
        print("\n-Test search no success")

    def test_search_results_view_context_posts(self):
        article = Article.objects.filter(slug="article-4-1")
        response = self.client.get(reverse("search_results") + "?q=foo")
        # workaround found in
        # https://stackoverflow.com/questions/17685023/
        # how-do-i-test-django-querysets-are-equal
        self.assertQuerySetEqual(
            response.context["articles"], article, transform=lambda x: x
        )
        print("\n-Test search equal querysets")

    def test_generate_unique_slug(self):
        self.assertEqual(generate_unique_slug(Article, "Article-4-1"), "article-4-1-1")
        print("\n-Test generate unique slug")
