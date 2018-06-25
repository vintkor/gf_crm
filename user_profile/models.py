from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext as _
from .managers import UserManager
from geo.models import Region


class Status(models.Model):
    """
    Модель с должностями сотрудников
    """
    title = models.CharField(verbose_name=_('Название'), max_length=250)
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))

    class Meta:
        verbose_name = _('Статус')
        verbose_name_plural = _('Статусы')

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    """
    Пользователи системы
    """
    email = models.EmailField(verbose_name=_('email'), max_length=255, unique=True, db_index=True)
    avatar = models.ImageField('Аватар', blank=True, null=True, upload_to="user/avatar")
    first_name = models.CharField(_('Фамилия'), max_length=40, null=True, blank=True)
    last_name = models.CharField(_('Имя'), max_length=40, null=True, blank=True)
    date_of_birth = models.DateField(_('Дата рождения'), null=True, blank=True)
    rate_per_hour = models.PositiveSmallIntegerField(verbose_name=_('Ставка за час (USD)'))
    status = models.ManyToManyField(Status, verbose_name=_('Статус'))
    is_active = models.BooleanField(_('Активен'), default=True)
    is_admin = models.BooleanField(_('Суперпользователь'), default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.email

    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        elif self.first_name:
            return '{} {}'.format(self.first_name, self.email)
        elif self.last_name:
            return '{} {}'.format(self.last_name, self.email)
        else:
            return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def is_client(self):
        """
        Пользователь является клиентом
        :return: bool
        """
        return True if self.client else False


class Source(models.Model):
    """
    Источник - откуда зашёл клиент в компанию
    """
    title = models.CharField(verbose_name=_('Название'), max_length=250)
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))

    class Meta:
        verbose_name = _('Источник клиента')
        verbose_name_plural = _('Источники клиентов')

    def __str__(self):
        return self.title


class Client(models.Model):
    """
    Только клиенты компании
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    country = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('Страна'))
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name=_('Источник клиента'))

    class Meta:
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')

    def __str__(self):
        return self.user.__str__()
