from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views.establishment import EstablishmentReadonlyModelViewSet
from api.views.records import RecordAPIView
from api.views.handle_request import HandleRequestAPIView

establishment_router = SimpleRouter()
establishment_router.register(r'establishment', EstablishmentReadonlyModelViewSet)

urlpatterns = [
    path('', include(establishment_router.urls)),
    path('establishment/<int:establishment_id>/record', RecordAPIView.as_view()),
    path('establishment/<int:establishment_id>/handle', HandleRequestAPIView.as_view()),
]
