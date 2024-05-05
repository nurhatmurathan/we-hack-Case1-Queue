from django.urls import path, include

from api.views.consultant import (
    ConsultantClientsListAPIView,
    ConsultantClientsUpdateAPIView
)

urlpatterns = [
    path('consultants/admin/clients', ConsultantClientsListAPIView.as_view()),
    path('consultants/admin/clients/<int:client_id>', ConsultantClientsUpdateAPIView.as_view()),
]
