from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from reminder.models import ChecklistItem, ChecklistItemHistory


@receiver(pre_save, sender=ChecklistItem)
def checklistitem_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        # Новый объект: нет старого экземпляра
        instance._old_instance = None
    else:
        try:
            instance._old_instance = ChecklistItem.objects.get(pk=instance.pk)
        except ChecklistItem.DoesNotExist:
            instance._old_instance = None


@receiver(post_save, sender=ChecklistItem)
def checklistitem_post_save(sender, instance, created, **kwargs):
    if created:
        ChecklistItemHistory.objects.create(item=instance, action='created')
        return
    old = getattr(instance, '_old_instance', None)
    if not old:
        return
    if old.completed != instance.completed:
        ChecklistItemHistory.objects.create(
            item=instance,
            action='completed' if instance.completed else 'uncompleted'
        )
    if old.archived != instance.archived:
        ChecklistItemHistory.objects.create(
            item=instance,
            action='archived' if instance.archived else 'unarchived'
        )
    if old.priority_id != instance.priority_id:
        old_priority_name = old.priority.name if old.priority else '-'
        new_priority_name = instance.priority.name if instance.priority else '-'
        ChecklistItemHistory.objects.create(
            item=instance,
            action='moved',
            details=f'Изменение приоритета: {old_priority_name} -> {new_priority_name}'
        )