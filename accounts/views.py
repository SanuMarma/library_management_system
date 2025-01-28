from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from transactions.models import Transaction

# Create your views here.   

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form) 
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('homepage')
    
class UserLogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('homepage')
    

class Profile(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'accounts/profile.html'
    balance = 0
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account, transaction_type=2).select_related('book')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
    