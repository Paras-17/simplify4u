from django.urls import path
from .views import summarize_view, translate_view, analyze_view

urlpatterns = [
    path('summarize/', summarize_view, name='summarize'),
    path('translate/', translate_view, name='translate'),
    path('analyze/', analyze_view, name='analyze'),
]
