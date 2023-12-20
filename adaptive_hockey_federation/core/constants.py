NAME_MAX_LENGTH = 256
EMAIL_MAX_LENGTH = 256
QUERY_SET_LENGTH = 15
TEST_USERS_AMOUNT = 3
DB_MESSAGE = 'Данные успешно добавлены!'

ROLE_AGENT = 'agent'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'
ROLES_CHOICES = (
    (ROLE_AGENT, 'Представитель команды'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
)
