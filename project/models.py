from django.db import models
from django.utils.translation import ugettext as _
from user_profile.models import Client
from user_profile.models import User
from settings.models import Setting
from ckeditor_uploader.fields import RichTextUploadingField


class Status(models.Model):
    """
    Статусы проектов
    """
    title = models.CharField(max_length=200, verbose_name=_('Статус'))
    description = RichTextUploadingField(verbose_name=_('Описание'), blank=True, null=True)
    order = models.PositiveSmallIntegerField(verbose_name=_('Порядок сортировки'), default=100)

    class Meta:
        verbose_name = _('Статус проекта')
        verbose_name_plural = _('Статусы проектов')
        ordering = ('order',)

    def __str__(self):
        return self.title


class Project(models.Model):
    """
    Проект
    """
    title = models.CharField(verbose_name=_('Название'), max_length=250)
    description = RichTextUploadingField(verbose_name=_('Описание'), blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('Клиент'))
    pm = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name=_('Проект менеджер'), blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))
    date_start = models.DateField(blank=True, null=True, verbose_name=_('Дата старта проекта'))
    date_end = models.DateField(blank=True, null=True, verbose_name=_('Дата сдачи проекта'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('Проект')
        verbose_name_plural = _('проекты')

    def __str__(self):
        return self.title

    def get_percent(self):
        """
        Процент выполнения проекта
        :return: float
        """

        milestones = self.milestone_set.all()
        percents = []
        count_milestones = 0

        for ind, milestone in enumerate(milestones):
            percents.append(milestone.get_percent())
            count_milestones = ind + 1

        avg_percent = sum(percents) / count_milestones if count_milestones > 0 else 0
        return round(avg_percent, 1)


class Milestone(models.Model):
    """
    Майлстоун - состоит из модулей
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Проект'))
    index_number = models.PositiveSmallIntegerField(verbose_name=_('Порядковый номер'))
    amount_of_days = models.PositiveSmallIntegerField(verbose_name=_('Количество дней'))
    date_start = models.DateField(blank=True, null=True, verbose_name=_('Дата старта майстоуна'))

    class Meta:
        verbose_name = _('Майлстоун')
        verbose_name_plural = _('Майлстоуны')
        ordering = ('index_number',)

    def __str__(self):
        return 'Milestone #{}'.format(self.index_number)

    def get_percent(self):
        """
        Процент выполнения майлстоуна
        :return: float
        """

        modules = self.module_set.all()
        percents = []
        count_modules = 0

        for ind, module in enumerate(modules):
            percents.append(module.get_percent())
            count_modules = ind + 1

        avg_percent = sum(percents) / count_modules if count_modules > 0 else 0
        return round(avg_percent, 1)


class Module(models.Model):
    """
    Модуль - состоит из задач
    """
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, verbose_name=_('Майлстоун'))
    title = models.CharField(verbose_name=_('Название'), max_length=250)
    description = RichTextUploadingField(verbose_name=_('Описание'), blank=True, null=True)
    order = models.PositiveSmallIntegerField(verbose_name=_('Порядок сортировки'), default=100)

    class Meta:
        verbose_name = _('Модуль')
        verbose_name_plural = _('Модули')
        ordering = ('order',)

    def __str__(self):
        return self.title

    def get_price(self):
        """
        Цена модуля
        :return: int
        """
        return sum([i.get_price() for i in self.task_set.all()])

    get_price.short_description = _('Цена модуля')

    def get_percent(self):
        """
        Процент выполнения модуля
        :return: float
        """

        tasks = self.task_set.all()
        count_tasks = tasks.count()
        tasks_is_done = tasks.filter(status=3).count()
        percent = (tasks_is_done * 100) / count_tasks if count_tasks != 0 else 100
        return round(float(percent), 1)


STATUS_CHOICES = (
    ('1', _('К выполнению')),
    ('2', _('На проверку')),
    ('3', _('Выполнено')),
)


class Task(models.Model):
    """
    Задача - самое маленькое звено
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name=_('Модуль'))
    title = models.CharField(verbose_name=_('Название'), max_length=250)
    description = RichTextUploadingField(verbose_name=_('Описание'), blank=True, null=True)
    collaborator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Исполнитель'))
    time = models.PositiveSmallIntegerField(verbose_name=_('Кол-во часов для выполнения'))
    rate_per_hour = models.PositiveSmallIntegerField(verbose_name=_('Ставка за час (USD)'), blank=True, null=True)
    order = models.PositiveSmallIntegerField(verbose_name=_('Порядок сортировки'), default=100)
    status = models.CharField(max_length=2, verbose_name=_('Статус'), choices=STATUS_CHOICES, default=1)

    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')
        ordering = ('order',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Если не установлена цена за час -> будет установлена цена за час исполнителя
        # Если цена исполнителя не указана -> будет установлена стандартная цена из настроек
        if self.rate_per_hour is None:
            if self.collaborator:
                self.rate_per_hour = self.collaborator.rate_per_hour
            else:
                self.rate_per_hour = Setting.objects.first().rate_per_hour
        return super(Task, self).save(*args, **kwargs)

    def get_price(self):
        """
        Цена задачи
        :return: int
        """
        return self.rate_per_hour * self.time if (self.time and self.rate_per_hour) else 0

    get_price.short_description = _('Цена задачи')

    def is_completed(self):
        return True if self.status == '3' else False

    def is_on_verify(self):
        return True if self.status == '2' else False


class Comment(models.Model):
    """
    Комментарии задачи
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('Задача'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Пользователь'))
    text = RichTextUploadingField(verbose_name=_('Текс'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')

    def __str__(self):
        return self.text[:100]
