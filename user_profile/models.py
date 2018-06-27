from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext as _
from .managers import UserManager
from geo.models import Region


class User(AbstractBaseUser, PermissionsMixin):
    """
    Пользователи системы
    """
    email = models.EmailField(verbose_name=_('email'), max_length=255, unique=True, db_index=True)
    avatar = models.ImageField('Аватар', blank=True, null=True, upload_to="user/avatar")
    first_name = models.CharField(_('Фамилия'), max_length=40, null=True, blank=True)
    last_name = models.CharField(_('Имя'), max_length=40, null=True, blank=True)
    date_of_birth = models.DateField(_('Дата рождения'), null=True, blank=True)
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


class Technology(models.Model):
    """
    Технологии
    """
    title = models.CharField(verbose_name=_('Название'), max_length=250)
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)

    class Meta:
        verbose_name = _('Технология')
        verbose_name_plural = _('Технологии')

    def __str__(self):
        return self.title


class Developer(models.Model):
    """
    Разработчики
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    rate_per_hour = models.PositiveSmallIntegerField(verbose_name=_('Ставка за час (USD)'))
    technology = models.ManyToManyField(Technology, through='user_profile.DeveloperTechnology')

    class Meta:
        verbose_name = _('Разработчик')
        verbose_name_plural = _('Разработчики')

    def __str__(self):
        return self.user.get_short_name()


EXPERIENCE_CHOICES = (
    ('1', _('1')),
    ('2', _('2')),
    ('3', _('3')),
    ('4', _('4')),
    ('5', _('5')),
)


class DeveloperTechnology(models.Model):
    """
    Технологии которыми владеет разработчик
    """
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name=_('Разработчик'))
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE, verbose_name=_('Технология'))
    experience = models.CharField(verbose_name=_('Квалификация'), max_length=1, choices=EXPERIENCE_CHOICES)

    class Meta:
        verbose_name = _('Технология котой владеет разработчик')
        verbose_name_plural = _('Технологии которыми владеет разработчик')

    def __str__(self):
        return '{} > {}'.format(self.developer, self.experience)


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


class ClientStatus(models.Model):
    """
    Статусы клиента
    """
    title = models.CharField(verbose_name=_('Название'), max_length=250)
    order = models.CharField(verbose_name=_('Сортировка'), default=10, max_length=200)

    class Meta:
        verbose_name = _('Статус клиента')
        verbose_name_plural = _('Статусы клиентов')
        ordering = ('order',)

    def __str__(self):
        return self.title


class Client(models.Model):
    """
    Только клиенты компании
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    country = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('Страна'))
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name=_('Источник клиента'))
    manager = models.ManyToManyField(User, related_name='managers', verbose_name=_('Менеджер'))
    status = models.ForeignKey(ClientStatus, on_delete=models.SET_NULL, verbose_name=_('Статус'), blank=True, null=True)

    class Meta:
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')

    def __str__(self):
        return self.user.__str__()
