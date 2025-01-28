from django.db import models
from django.contrib.auth.models import User
from categories.models import Category

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    borrow_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/media/uploads/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateField(auto_now_add=True)
        
    def __str__(self):
        return f"Reviews by {self.user}"

