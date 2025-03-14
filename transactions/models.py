from django.db import models

# Create your models here.
from django.db import models
from accounts.models import UserAccount
from books.models import Book
from .constants import TRANSACTION_TYPE

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, related_name='transactions', on_delete=models.CASCADE) 
    
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    book = models.ForeignKey(Book, related_name='transactions',  on_delete=models.CASCADE, default=1) 

    
    class Meta:
        ordering = ['timestamp'] 

