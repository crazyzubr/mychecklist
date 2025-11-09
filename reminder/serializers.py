from rest_framework import serializers
from .models import ChecklistItem, Priority


class ChecklistItemSerializer(serializers.ModelSerializer):
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())
    # completed = serializers.SerializerMethodField()

    class Meta:
        model = ChecklistItem
        fields = [
            'id', 'text', 'planned_date', 'priority', 'percentage', 'completed', 'archived']
        read_only_fields = ['id', 'archived', 'completed']

    # def get_completed(self, obj) -> bool:
    #     return obj.completed
