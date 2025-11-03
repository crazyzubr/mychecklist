from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from reminder.models import Priority, ChecklistItem
import json


def main_view(request):
    priorities = Priority.objects.order_by('level')
    # Для каждой колонки берем активные (неархивированные) элементы
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


@require_POST
def add_item(request):
    data = json.loads(request.body)
    text = data.get('text')
    planned_date = data.get('planned_date')
    priority_id = data.get('priority_id')
    if not text or not planned_date or not priority_id:
        return JsonResponse({'error': 'Недостаточно данных'}, status=400)
    item = ChecklistItem.objects.create(
        text=text,
        planned_date=planned_date,
        priority_id=priority_id,
        completed=False,
        archived=False,
    )
    return JsonResponse({
        'id': item.id,
        'text': item.text,
        'planned_date': item.planned_date.strftime('%Y-%m-%d'),
        'completed': item.completed,
        'archived': item.archived,
    })


@require_POST
def toggle_completed(request, item_id):
    item = get_object_or_404(ChecklistItem, id=item_id, archived=False)
    item.completed = not item.completed
    item.save()
    return JsonResponse({'completed': item.completed})


@require_POST
def remove_item(request, item_id):
    item = get_object_or_404(ChecklistItem, id=item_id, archived=False)
    item.archived = True
    item.save()
    return JsonResponse({'archived': True})
