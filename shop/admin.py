from django.contrib import admin
from .models import Book, Order, Cart, Report


admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Report)
