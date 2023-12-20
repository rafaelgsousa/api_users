from django.contrib import admin

from users.models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'email', 'phone',
    ordering = '-id',
    search_fields = 'id', 'first_name', 'email',
    list_per_page = 10