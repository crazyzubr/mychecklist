from django.db import models
from django.utils import timezone


class Priority(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    level = models.PositiveIntegerField('Уровень', unique=True)

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'
        ordering = ['level']

    def __str__(self):
        return f'{self.name} ({self.level})'


class ChecklistItem(models.Model):
    text = models.TextField('Текст')
    planned_date = models.DateField('Планируемая дата завершения')
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, verbose_name='Приоритет')
    completed = models.BooleanField('Выполнено', default=False)
    archived = models.BooleanField('Архивирован', default=False)
    completion_date = models.DateTimeField('Дата завершения', null=True, blank=True)

    class Meta:
        verbose_name = 'Элемент чеклиста'
        verbose_name_plural = 'Элементы чеклиста'

    def save(self, *args, **kwargs):
        if self.completed and not self.completion_date:
            self.completion_date = timezone.now()
        elif not self.completed:
            self.completion_date = None
        super().save(*args, **kwargs)
