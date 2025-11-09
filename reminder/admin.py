from django.contrib import admin

from reminder.models import Priority, ChecklistItem, ChecklistItemHistory, ChecklistGroup


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    pass


class ChecklistItemHistoryInline(admin.TabularInline):
    model = ChecklistItemHistory
    extra = 0
    readonly_fields = ('action', 'created_at', 'details')
    can_delete = False


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemHistoryInline]
    list_display = ('id', 'text', 'priority', 'created_at', 'percentage', 'completed', 'archived')
    list_filter = ('priority', 'created_at')
    search_fields = ('text',)
    date_hierarchy = 'created_at'


@admin.register(ChecklistGroup)
class ChecklistGroupAdmin(admin.ModelAdmin):
    pass
