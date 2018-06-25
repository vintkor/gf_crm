from django.db import models
from django.utils.translation import ugettext as _


class Region(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Название'))
    code = models.CharField(max_length=15, blank=True, null=True, unique=True, verbose_name=_('Код региона'))

    class Meta:
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('catalog-category', args=[self.slug])