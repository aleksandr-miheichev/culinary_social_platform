from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db.models import CharField, EmailField, UniqueConstraint

from users.validators import validate_username


class CustomUser(AbstractUser):
    username = CharField(
        max_length=settings.MAX_LENGTH_TEXT_USERS,
        unique=True,
        validators=[validate_username, ],
        verbose_name='Логин пользователя',
        help_text='Введите свой логин',
    )
    first_name = CharField(
        max_length=settings.MAX_LENGTH_TEXT_USERS,
        verbose_name='Имя пользователя',
        help_text='Введите имя',
    )
    last_name = CharField(
        max_length=settings.MAX_LENGTH_TEXT_USERS,
        verbose_name='Фамилия пользователя',
        help_text='Введите фамилию',
    )
    email = EmailField(
        max_length=settings.MAX_LENGTH_EMAIL,
        validators=[EmailValidator],
        unique=True,
        verbose_name='Электронная почта пользователя',
        help_text='Введите свою электронную почту',
    )
    password = CharField(
        max_length=settings.MAX_LENGTH_TEXT_USERS,
        verbose_name='Пароль пользователя',
        help_text='Введите свой пароль',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

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
            f'электронная почта - "{self.email}"'
        )
