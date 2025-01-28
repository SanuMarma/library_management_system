from django.shortcuts import render
from django.shortcuts import get_object_or_404
from books.models import Book
from categories.models import Category
from django.views.generic import ListView

class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'data'
    model = Book

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            return Book.objects.filter(category=category)
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context
