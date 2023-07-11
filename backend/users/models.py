from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username

# USER = 'user'
# ADMIN = 'admin'
# MODERATOR = 'moderator'

# ROLE_CHOICES = [
#     (USER, USER),
#     (ADMIN, ADMIN),
#     (MODERATOR, MODERATOR)
# ]


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Подписан'
    )

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]
