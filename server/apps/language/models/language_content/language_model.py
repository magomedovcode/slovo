from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator
)


class Language(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Название языка'),
        help_text=_('Введите название языка'),
    )
    description = models.TextField(
        verbose_name=_('Описание языка'),
        help_text=_('Введите описание языка')
    )
    code = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_('Код языка'),
        help_text=_('Код языка в формате ГОСТ 7.75-97 (латинский)'),
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(3),
        ]
    )

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = _('Язык')
        verbose_name_plural = _('Языки')
        ordering = ['id']

    def __str__(self):
        return self.name
