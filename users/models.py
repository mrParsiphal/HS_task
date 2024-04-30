from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class UserProfile(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=18, unique=True, verbose_name='Номер телефона / Логин')
    invite_code = models.CharField(max_length=6, unique=True, null=True, blank=True, verbose_name='Инвайт-код')
    subscription = models.CharField(max_length=6, null=True, verbose_name='Инвайт-код, на который подписаны')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персонала')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Invite_code_bindings(models.Model):
    user_invite_code = models.OneToOneField(UserProfile, on_delete=models.DO_NOTHING, related_name='user_invite_code',
                                            verbose_name='Пользователь')
    invited_user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name='invited_users',
                                      null=True, verbose_name='Подписка')

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return 'Связь ' + str(self.pk)