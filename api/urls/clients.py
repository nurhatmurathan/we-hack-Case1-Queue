from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views.records import ClientDetailView

urlpatterns = [
    path('clients/<str:iin>/', ClientDetailView.as_view(), name='client-detail'),
]
