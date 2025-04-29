from django.urls import path
from .views import SystemStatsView

urlpatterns = [
    path('stats/', SystemStatsView.as_view(), name='system_stats'),
]
