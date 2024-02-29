import pytest

test_password = "admin"
test_name = "admin"
test_lastname = "admin"
test_role_admin = "admin"
test_role_user = "user"
test_email = "admin@admin.ru"


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        password=test_password,
        first_name=test_name,
        last_name=test_lastname,
        role=test_role_admin,
        email=test_email,
    )


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def adminuser(djangousermodel):
    admin = djangousermodel.objects.createsuperuser(
        first_name="admin", email="admin@admin.com", password="admin"
    )
    admin.isstaff = True
    admin.issuperuser = True
    admin.save()
    return admin


@pytest.fixture
def moderatoruser(djangousermodel):
    moderator = djangousermodel.objects.createuser(
        first_name="moderator",
        email="moderator@moderator.com",
        password="moderator",
    )
    return moderator
