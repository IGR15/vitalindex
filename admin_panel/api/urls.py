from django.urls import path
from .views import (
    SystemStatsView,
    UserActivityView,
    UserRoleStatsView,
    RecentActivityView,
    ServerHealthView
)

urlpatterns = [
    path('stats/', SystemStatsView.as_view(), name='system_stats'),
    path('user-activity/', UserActivityView.as_view(), name='user_activity'),
    path('user-roles/', UserRoleStatsView.as_view(), name='user_role_stats'),
    path('recent-activity/', RecentActivityView.as_view(), name='recent_activity'),
    path('server-health/', ServerHealthView.as_view(), name='server_health'),
]