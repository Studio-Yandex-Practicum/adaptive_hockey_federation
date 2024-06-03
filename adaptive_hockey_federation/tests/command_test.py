import pytest

from main.data_factories.factories import TeamFactory
from main.models import Team
from users.factories import UserFactory


@pytest.fixture
def create_user():
    return UserFactory()


@pytest.fixture
def create_team(create_user):
    return TeamFactory(curator=create_user)


@pytest.mark.django_db
def test_create_team(create_team):
    assert create_team is not None, "Не удалось создать команду"


@pytest.mark.django_db
def test_read_team(create_team):
    # TODO: Добавить проверку пермишенов для чтения команды
    team_id = create_team.id
    read_team = Team.objects.filter(pk=team_id).first()
    assert read_team is not None, "Не удалось считать информацию о команде"


@pytest.mark.django_db
def test_update_team(create_team):
    # TODO: Добавить проверку пермишенов для обновления команды
    new_team_name = "Updated Team"
    create_team.name = new_team_name
    create_team.save()
    updated_team = Team.objects.get(pk=create_team.pk)
    assert updated_team.name == new_team_name, "Не удалось обновить команду"


@pytest.mark.django_db
def test_delete_team(create_team):
    # TODO: Добавить проверку пермишенов для удаления команды
    team_id = create_team.id
    create_team.delete()
    deleted_team = Team.objects.filter(pk=team_id).first()
    assert deleted_team is None, "Не удалось удалить команду"
