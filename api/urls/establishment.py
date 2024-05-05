from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views.establishment import EstablishmentReadonlyModelViewSet

establishment_router = SimpleRouter()
establishment_router.register(r'establishment', EstablishmentReadonlyModelViewSet)

urlpatterns = [
    path('', include(establishment_router.urls))
]
