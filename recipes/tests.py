from django.test import TestCase
from django.urls import reverse


class RecipeURLSTest(TestCase):
    def test_recipe_home_url_is_correct(self) -> None:
        home_url = reverse("recipes:home")
        self.assertEqual(home_url, "/")
