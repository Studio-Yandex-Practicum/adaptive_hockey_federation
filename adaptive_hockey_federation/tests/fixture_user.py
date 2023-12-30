import pytest

test_password = 'admin'
test_name = 'admin'
test_lastname = 'admin'
test_role = 'admin'
test_email = 'admin@admin.ru'


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        password=test_password,
        first_name=test_name,
        last_name=test_lastname,
        role=test_role,
        email=test_email,
    )


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client
