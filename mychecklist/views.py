from django.shortcuts import render
from django.utils import timezone

from reminder.models import ChecklistGroup, Priority, ChecklistItem


def main_view(request):
    priorities = Priority.objects.order_by('level')
    checklist_items = (
        ChecklistItem.objects
        .filter(archived=False)
        .select_related('priority')
        .order_by('planned_date', 'created_at')
    )
    items_by_priority = {p.id: [] for p in priorities}

    for item in checklist_items:
        items_by_priority[item.priority_id].append(item)

    # Сортируем: не выполненные сверху, выполненные вниз
    for p_id in items_by_priority:
        items_by_priority[p_id].sort(key=lambda x: x.completed)

    return render(request, 'index.html', {
        'priorities': priorities,
        'items_by_priority': items_by_priority,
    })

def group_checklists_view(request):
    groups = ChecklistGroup.objects.all().order_by('from_date_index', 'end_date_index')
    groups_data = []
    for group in groups:
        priorities = Priority.objects.all().order_by('level')
        columns = []
        for priority in priorities:
            items = ChecklistItem.objects.filter(
                planned_date__gte=group.date_from,
                planned_date__lte=group.date_to,
                priority=priority,
                archived=False,
            ).order_by('planned_date', 'created_at')
            columns.append({
                'priority': priority,
                'items': items,
            })
        groups_data.append({
            'group': group,
            'columns': columns,
        })
    return render(request, 'groups.html', {'groups_data': groups_data})
