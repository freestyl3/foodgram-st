from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model


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
    email = models.EmailField(
        verbose_name='Эл. почта',
        unique=True
    )
    avatar = models.ImageField(
        verbose_name='Аватар пользователя',
        upload_to='media/users/avatars/',
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
        ordering = ('user', )