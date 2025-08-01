from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewTest(RecipeTestBase):
    def tearDown(self):
        return super().tearDown()

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse("recipes:home")
        )
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "<h1>No Recipes found here 😢</h1>",
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_load_recipes(self):
        # Need a recipe for this test
        self.make_recipe()
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published=False"""

        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:home"))

        self.assertIn(
            "<h1>No Recipes found here 😢</h1>",
            response.content.decode('utf-8')
        )

    # @patch('recipes.views.PER_PAGE', new=3)
    # def test_recipe_home_is_paginated(self):
    #     for i in range(9):
    #         kwargs = {
    #                 'slug': f'r{i}',
    #                 'author_data': {'username': f'u{i}'}
    #             }
    #         self.make_recipe(**kwargs)

    #     response = self.client.get(reverse("recipes:home"))
    #     recipes = response.context['recipes']
    #     paginator = recipes.paginator

    #     self.assertEqual(paginator.num_pages, 3)

    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(9)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse("recipes:home") + '?page=1A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse("recipes:home") + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
