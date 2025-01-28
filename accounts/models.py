from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAccount(models.Model):
    user=models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    def __str__(self):
        return str(self.user)
