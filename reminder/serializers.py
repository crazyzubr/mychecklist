from rest_framework import serializers
from .models import ChecklistItem, Priority


class ChecklistItemSerializer(serializers.ModelSerializer):
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())

    class Meta:
        model = ChecklistItem
        fields = [
            'id', 'text', 'planned_date', 'priority', 'percentage', 'completed', 'archived']
        read_only_fields = ['id', 'archived', 'completed']
