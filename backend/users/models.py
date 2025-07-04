from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class FoodgramUser(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=150,
        validators=[
            RegexValidator(
                regex=(r"^[\w.@+-]+$")
            )
        ],
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
        null=False
    )
    email = models.EmailField(
        verbose_name='Эл. почта',
        unique=True
    )
    avatar = models.ImageField(
        verbose_name='Аватар пользователя',
        upload_to='users/avatars/',
        default=None,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    follower = models.ForeignKey(
        get_user_model(),
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='followers'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user', )
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'follower'],
                name='unique subsctiption'
            )
        ]

    def __str__(self):
        user = self.user.username
        follower = self.follower.username
        

        return f'{follower} подписан на {user}'
