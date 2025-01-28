from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render
from django.contrib import messages
from accounts.models import UserAccount
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from transactions.constants import DEPOSIT, BORROW, RETURN
from datetime import datetime
from django.db.models import Sum
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from transactions.forms import (
    DepositForm,
    BorrowBookForm,
)
from transactions.models import Transaction
from books.models import Book

# Create your views here.

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'
    
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposite Message", "transactions/deposite_email.html")
        return super().form_valid(form)
    
    
class BorrowBookView(TransactionCreateMixin):
    template_name = 'transactions/borrow_book.html'
    form_class = BorrowBookForm
    title = 'Borrow Book'

    def get_initial(self):
        initial = {'transaction_type': BORROW}
        return initial
    
    def post(self, request, id):
        book = get_object_or_404(Book, id=id)
        account = self.request.user.account

        if account.balance >= book.borrow_price:

            account.balance -= book.borrow_price
            account.save(update_fields=['balance'])

            Transaction.objects.create(account=request.user.account, amount=book.borrow_price, balance_after_transaction=account.balance, transaction_type=BORROW, book=book)


            messages.success(
                self.request,
                f'{book.title} has been borrowed successfully for {"{:,.2f}".format(float(book.borrow_price))}$.'
            )

            send_transaction_email(self.request.user, book.title, "Borrow Book", "transactions/borrow_email.html")
            return redirect('transaction_report')
        else:
            return render(request, 'home.html')
        

class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
            
        })

        return context


class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, borrow_id):
        transaction = get_object_or_404(Transaction, id=borrow_id)

        if transaction.transaction_type == RETURN:
            messages.info(request, "This book has already been returned.")
            return redirect('transaction_report')
        
        user_account = transaction.account
        user_account.balance += transaction.amount
        user_account.save()

        transaction.balance_after_transaction = user_account.balance
        transaction.transaction_type = RETURN
        transaction.save()

        messages.success(request, f'Book return successfully processed!')

        return redirect('transaction_report')


class BookListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'transactions/borrow_books_list.html'
    context_object_name = 'Books' 
    balance = 0
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account, transaction_type=2)
        return queryset

