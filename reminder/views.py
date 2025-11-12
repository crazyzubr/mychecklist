from django.db import transaction
from django.db.models import F
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Priority, ChecklistItem
from .serializers import ChecklistItemSerializer
from django.shortcuts import get_object_or_404


class ChecklistMainView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        priorities = Priority.objects.order_by('level')
        data = []
        for priority in priorities:
            items = ChecklistItem.objects.filter(
                priority=priority, archived=False).order_by('percentage')
            serializer = ChecklistItemSerializer(items, many=True)
            data.append({
                'priority': {'id': priority.id, 'name': priority.name, 'level': priority.level},
                'items': serializer.data,
            })
        return Response(data, content_type='application/json')


class ChecklistItemCreateView(APIView):

    def post(self, request):
        print(request.data)
        serializer = ChecklistItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(archived=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChecklistItemToggleCompletedView(APIView):

    def post(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk, archived=False)
        item.percentage = 0 if item.completed else 100
        item.save()
        serializer = ChecklistItemSerializer(item)
        return Response(serializer.data)


class ChecklistItemArchiveView(APIView):

    def post(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk, archived=False)
        item.archived = True
        item.save()
        return Response({'archived': True})


class ChecklistItemMoveView(APIView):

    def post(self, request):
        """
        Ожидает JSON с:
        - id (int): ID перемещаемого элемента
        - priority (int): ID приоритета колонки, куда переместить
        - order (int): новая позиция в колонке (от 0)
        """
        data = request.data
        item_id = data.get('id')
        new_priority_id = data.get('priority')
        new_order = data.get('order')

        if item_id is None or new_priority_id is None or new_order is None:
            return Response({'error': 'id, priority и order обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(ChecklistItem, pk=item_id)

        # Обновляем priority и порядок (order)
        # Нужно в модели добавить поле order = PositiveIntegerField(default=0), если его нет

        with transaction.atomic():
            # Сдвигаем другие элементы в целевой колонке, которые идут >= new_order
            ChecklistItem.objects.filter(
                priority_id=new_priority_id,
                order__gte=new_order
            ).exclude(pk=item.pk).update(order=F('order') + 1)

            # При этом сдвигаем назад элементы колонки старой, если меняется колонка
            if item.priority_id != new_priority_id:
                ChecklistItem.objects.filter(
                    priority_id=item.priority_id,
                    order__gt=item.order
                ).update(order=F('order') - 1)

            # Обновляем перемещаемый элемент
            item.priority_id = new_priority_id
            item.order = new_order
            item.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class ChecklistItemEditAPIView(APIView):

    def get(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk)
        return Response(ChecklistItemSerializer(item).data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk)
        serializer = ChecklistItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
