from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # date_hierarchy = 'date_joined'
    list_display = (
        'id',
        'username',
        'email',
        'phone',
        'first_name',
        'last_name',
        'role',
        'team',
    )
    fields = [
        'username',
        'email',
        'phone',
        ('first_name', 'last_name'),
        'role',
        'team',
    ]
    empty_value_display = '-пусто-'
