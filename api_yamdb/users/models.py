from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    """Модель user."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES_ROLES = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    ]
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    role = models.CharField(
        verbose_name='Статус',
        max_length=20,
        choices=CHOICES_ROLES,
        default=USER
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    @property
    def is_admin(self):
        return (self.role == self.ADMIN or self.is_superuser)

    @property
    def is_moderator(self):
        return (self.role == self.MODERATOR)

    @property
    def is_user(self):
        return (self.role == self.USER)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
