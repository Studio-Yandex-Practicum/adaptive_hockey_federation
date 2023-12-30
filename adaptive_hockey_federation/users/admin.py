from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.models import Group, Permission
from users.forms import GroupAdminForm
from users.models import ProxyGroup, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # date_hierarchy = 'date_joined'
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'phone',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        "groups",
        "is_active",
    )
    fields = [
        ('first_name', 'last_name'),
        'email',
        'phone',
        'is_staff',
        'is_superuser',
        'role',
    ]
    empty_value_display = '-пусто-'

    @admin.display(description="Роль")
    def role(self, obj):
        return obj.groups.all()[:1]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("groups")


class HiddenAdmin(DjangoGroupAdmin):
    """Удаление модели из панели администратора.

    Необходимость регистрации модели в панели администратора
    вызвана применением пакета django-filer
    """

    def has_module_permission(self, request):
        return False


admin.site.unregister(Group)
admin.site.register(Group, HiddenAdmin)


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ["name"]
    filter_horizontal = ("permissions",)


admin.site.register(ProxyGroup, GroupAdmin)


def permissions_new_unicode(self):
    # Перевод настроек доступа
    class_name = str(self.content_type)
    permissions_name = str(self.name)

    if "Can delete" in permissions_name:
        permissions_name = "разрешено удалять"
    elif "Can add" in permissions_name:
        permissions_name = "разрешено добавлять"
    elif "Can change" in permissions_name:
        permissions_name = "разрешено изменять"
    elif "Can view" in permissions_name:
        permissions_name = "разрешено просматривать"

    return "%s - %s" % (class_name.title(), permissions_name)


Permission.__str__ = permissions_new_unicode
