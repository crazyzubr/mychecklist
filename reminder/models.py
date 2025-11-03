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
    priority = models.ForeignKey('Priority', on_delete=models.PROTECT, verbose_name='Приоритет')
    completed = models.BooleanField('Выполнено', default=False)
    archived = models.BooleanField('Архивирован', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True)  # добавленное поле

    class Meta:
        verbose_name = 'Элемент чеклиста'
        verbose_name_plural = 'Элементы чеклиста'

    def __str__(self):
        return f'{self.planned_date}: {self.text}'


class ChecklistItemHistory(models.Model):
    ACTION_CHOICES = [
        ('created', 'Создано'),
        ('completed', 'Выполнено'),
        ('uncompleted', 'Не выполнено'),
        ('archived', 'Архивировано'),
        ('unarchived', 'Разархивировано'),
        ('moved', 'Перемещено'),
    ]

    item = models.ForeignKey(
        ChecklistItem, on_delete=models.CASCADE,
        related_name='history', verbose_name='Чеклист элемент')
    action = models.CharField('Действие', max_length=20, choices=ACTION_CHOICES)
    details = models.TextField('Дополнительная информация', blank=True, null=True)
    created_at = models.DateTimeField('Дата и время', auto_now_add=True)

    class Meta:
        verbose_name = 'История элемента чеклиста'
        verbose_name_plural = 'Истории элементов чеклиста'
        ordering = ['-created_at']

    def __str__(self):
        return f'Действие от {self.created_at.isoformat()}'