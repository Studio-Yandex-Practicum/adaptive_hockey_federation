def set_default_permission_group(sender, **kwargs) -> None:
    """Функция для назначение прав группам пользователей"""
    from django.contrib.auth.models import Permission
    from users.constants import AGENTS_PERMS, GROUP_NAMES, MODERATORS_PERMS
    from users.models import ProxyGroup
    for group in GROUP_NAMES:
        group_obj, created = ProxyGroup.objects.get_or_create(name=group)
        if group == "Администраторы":
            for perm in Permission.objects.all():
                group_obj.permissions.add(perm)
        elif group == "Модераторы":
            for codename in MODERATORS_PERMS:
                group_obj.permissions.add(Permission.objects.get(
                    codename=codename))
        elif group == "Представители команд":
            for codename in AGENTS_PERMS:
                group_obj.permissions.add(Permission.objects.get(
                    codename=codename))
        group_obj.save()


def set_permission_create_user(role, user):
    """
    Функция установки прав доступа после создания пользователя
    """
    from core.constants import GROUP_CHOICES
    from users.models import ProxyGroup
    user.is_staff = False
    if role == 'Администратор':
        user.is_staff = True
    user.save()
    group = ProxyGroup.objects.get(name=GROUP_CHOICES[role])
    user.groups.clear()
    user.groups.add(group)


def send_user_data_after_create(email, password):
    """
    Функция отправки логина и пароля пользователю после создания
    """
    from django.core.mail import send_mail
    send_mail(
        None,
        f"Ваш логин для входа на сайт: {email} временный пароль: { password }",
        'admin@admin.ru',
        [email],
        fail_silently=False,
    )
