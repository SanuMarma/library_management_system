from django.shortcuts import render, redirect
from . import forms
from .models import Book
from django.contrib import messages
from transactions.models import Transaction

# Create your views here.
from django.views.generic import DetailView

class DetailBookView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'books/book_details.html'

 
    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = self.request.user.account.user
            new_review.book = book

            borrowed = Transaction.objects.filter(account=self.request.user.account, transaction_type=2, book=book).exists()
            if not borrowed:
                messages.error(self.request, "You cannot review a book you haven't borrowed.")
                return redirect("detail_book", id=book.id)
            new_review.save()
            messages.success(self.request, "Your review has been submitted!")
        return self.get(request, *args, **kwargs)
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form = forms.ReviewForm()

        context['reviews'] = reviews
        context['review_form'] = review_form
        return context


