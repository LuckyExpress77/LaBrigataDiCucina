from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', views.RecipeCreateView.as_view(), name='recipe-new'),
    path('recipe/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add-comment'),
    path('recipe/<int:pk>/like/', views.like_recipe, name='like-recipe'),
]
