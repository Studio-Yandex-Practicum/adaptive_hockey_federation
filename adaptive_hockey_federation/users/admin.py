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
    )
    fields = [
        ('first_name', 'last_name'),
        'role',
        'email',
        'phone',
    ]
    empty_value_display = '-пусто-'
