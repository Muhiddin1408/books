from django.db import models
from account.models import User


class Book(models.Model):
    CATEGORY = (
        ('drama', 'DRAMA'),
        ('janr', 'JANR'),

    )
    name = models.CharField(max_length=125)
    category = models.CharField(max_length=125, choices=CATEGORY, default='drama')
    author = models.CharField(max_length=125)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='book')
    date_manufactured = models.IntegerField()
    price = models.IntegerField()
    residue = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('delivering', 'DELIVERING'),
        ('completed', 'COMPLETED'),
        ('not cancelled', 'NOT CANCELLED'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=16, default='pending')
    products = models.TextField()
    quantity = models.FloatField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    subtotel = models.FloatField(default=1)

    def __str__(self):
        return self.product.name


class Report(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.book.name
