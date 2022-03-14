from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


UserAdmin.fieldsets += (
    (None, {'fields': ('phone', 'address')}),
)

admin.site.register(User, UserAdmin)
