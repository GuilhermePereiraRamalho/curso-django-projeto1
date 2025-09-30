from rest_framework import test
from rest_framework import status

from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIV2Test(test.APITestCase, RecipeMixin):
    def test_recipe_api_list_returns_200_ok(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
