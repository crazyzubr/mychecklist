from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Priority, ChecklistItem
from .serializers import ChecklistItemSerializer
from django.shortcuts import get_object_or_404

class ChecklistMainView(APIView):
    def get(self, request):
        priorities = Priority.objects.order_by('level')
        data = []
        for priority in priorities:
            items = ChecklistItem.objects.filter(priority=priority, archived=False).order_by('completed')
            serializer = ChecklistItemSerializer(items, many=True)
            data.append({
                'priority': {'id': priority.id, 'name': priority.name, 'level': priority.level},
                'items': serializer.data,
            })
        return Response(data)


class ChecklistItemCreateView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ChecklistItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(completed=False, archived=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChecklistItemToggleCompletedView(APIView):
    def post(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk, archived=False)
        item.completed = not item.completed
        item.save()
        serializer = ChecklistItemSerializer(item)
        return Response(serializer.data)


class ChecklistItemArchiveView(APIView):
    def post(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk, archived=False)
        item.archived = True
        item.save()
        return Response({'archived': True})
