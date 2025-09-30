from rest_framework import test
from rest_framework import status

from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeMixin

from unittest.mock import patch


class RecipeAPIV2Test(test.APITestCase, RecipeMixin):
    def get_recipe_api_list(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        return response

    def test_recipe_api_list_returns_200_ok(self):
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    @patch(
        'recipes.views.api.RecipeAPIV2Pagination.page_size',
        new=7
    )
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_numbers_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_numbers_of_recipes)
        response = self.client.get(
            reverse('recipes:recipes-api-list') + '?page=1'
        )
        qtd_of_loaded_recipes = len(response.data.get('results'))
        self.assertEqual(
            wanted_numbers_of_recipes,
            qtd_of_loaded_recipes
        )

    def test_recipe_api_list_dont_load_recipes_not_published(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )
