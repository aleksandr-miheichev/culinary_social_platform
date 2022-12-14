from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db.models import CharField, EmailField, UniqueConstraint

from foodgram.settings import MAX_LENGTH_EMAIL, MAX_LENGTH_TEXT_USERS
from users.validators import validate_username

ADMIN = 'admin'
USER = 'user'


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    ]
    username = CharField(
        max_length=MAX_LENGTH_TEXT_USERS,
        unique=True,
        validators=[validate_username, ],
        verbose_name='Логин пользователя',
        help_text='Введите свой логин',
    )
    first_name = CharField(
        max_length=MAX_LENGTH_TEXT_USERS,
        verbose_name='Имя пользователя',
        help_text='Введите имя',
    )
    last_name = CharField(
        max_length=MAX_LENGTH_TEXT_USERS,
        verbose_name='Фамилия пользователя',
        help_text='Введите фамилию',
    )
    email = EmailField(
        max_length=MAX_LENGTH_EMAIL,
        validators=[EmailValidator],
        verbose_name='Электронная почта пользователя',
        help_text='Введите свою электронную почту',
    )
    role = CharField(
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль пользователя',
        help_text='Выберите роль для пользователя',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'username', ]

    class Meta:
        constraints = [
            UniqueConstraint(
                name='unique_email_user',
                fields=['email', 'username', ],
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return (
            f'У пользователя с логином "{self.username}": '
            f'электронная почта - "{self.email}" и роль - "{self.role}"'
        )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff
