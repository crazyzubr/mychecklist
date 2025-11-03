from django.contrib import admin

from reminder.models import Priority


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    pass