from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def tearDown(self):
        return super().tearDown()

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse("recipes:recipe", kwargs={"id": 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_load_the_correct_recipe(self):
        need_title = 'This is a detail page - It load one recipe'

        self.make_recipe(title=need_title)

        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={
                    'id': 1
                }
            )
        )
        content = response.content.decode('utf-8')

        self.assertIn(need_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published=False"""

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={
                    'id': recipe.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)
