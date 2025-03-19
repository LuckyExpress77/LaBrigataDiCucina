import os
import django
from django.conf import settings

# Set up Django's configuration to recognize your settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.django.laBrigataDiCucina.settings')

# Initialize Django
django.setup()
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Recipe, Comment

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testperson', password='Abcd1234')
        Recipe.objects.create(title='Pasta alla Bolognese', body='My grandmothers Bolognese recipe', author=user)

    def test_title_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_creation(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.title, 'Pasta alla Bolognese')
        self.assertTrue(isinstance(recipe.author, User))

class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testperson', password='Abcd1234')
        recipe = Recipe.objects.create(title='Pasta alla Bolognese', body='My grandmothers Bolognese recipe', author=user)
        Comment.objects.create(recipe=recipe, comment='Yummy!', author=user)

    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.comment, 'Yummy!')
        self.assertTrue(isinstance(comment.recipe, Recipe))

class RecipeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_recipes = 5
        user = User.objects.create_user(username='testperson', password='Abcd1234')
        for recipe_id in range(number_of_recipes):
            Recipe.objects.create(title=f'Recipe {recipe_id}', body='Some random body', author=user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['recipes']) == 5)

class RecipeDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testperson', password='Abcd1234')
        Recipe.objects.create(title='Pasta alla Bolognese', body='My grandmothers Bolognese recipe', author=user)

    def test_view_url_exists_at_des2ired_location(self):
        response = self.client.get('/recipes/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recipe-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')