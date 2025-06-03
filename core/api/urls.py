from django.urls import path
from core.api.views import SearchView

urlpatterns = [
    path('search/', SearchView.as_view(), name='global-search'),
]
