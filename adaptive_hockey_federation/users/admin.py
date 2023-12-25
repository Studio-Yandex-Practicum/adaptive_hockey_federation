from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # date_hierarchy = 'date_joined'
    list_display = (
        'id',
        'first_name',
        'last_name',
        'role',
        'email',
        'phone',
        'is_staff',
        'is_superuser'
    )
    fields = [
        ('first_name', 'last_name'),
        'role',
        'email',
        'phone',
        'is_staff',
        'is_superuser'
    ]
    empty_value_display = '-пусто-'
