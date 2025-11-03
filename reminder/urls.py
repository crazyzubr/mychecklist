from django.urls import path
from .views import (
    ChecklistMainView,
    ChecklistItemCreateView,
    ChecklistItemToggleCompletedView,
    ChecklistItemArchiveView,
)

urlpatterns = [
    path('checklist', ChecklistMainView.as_view(),
         name='checklist-main'),
    path('checklist/item', ChecklistItemCreateView.as_view(),
         name='checklist-item-create'),
    path('checklist/item/<int:pk>/toggle_completed',
         ChecklistItemToggleCompletedView.as_view(), name='checklist-item-toggle'),
    path('checklist/item/<int:pk>/archive',
         ChecklistItemArchiveView.as_view(), name='checklist-item-archive'),
]
