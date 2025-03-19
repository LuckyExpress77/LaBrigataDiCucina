from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from .models import Recipe, Comment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipeForm, CommentForm

class RecipeListView(generic.ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipe_list.html'
    paginate_by = 5

class RecipeDetailView(generic.DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

@method_decorator(login_required, name='dispatch')
class RecipeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'add_recipe.html'
    success_url = reverse_lazy('recipe-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'recipes/add_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.kwargs['pk']})

@login_required
def like_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return redirect('recipe-detail', pk=pk)

