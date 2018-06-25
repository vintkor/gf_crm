from django.db import models
from django.utils.translation import ugettext as _


class Setting(models.Model):
    """
    Системные настройки
    """
    rate_per_hour = models.PositiveSmallIntegerField(verbose_name=_('Цена за час (USD)'))

    class Meta:
        verbose_name = _('Системные настройки')
        verbose_name_plural = _('Системные настройки')

    def __str__(self):
        return 'Settings'
