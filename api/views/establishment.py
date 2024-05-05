from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers.esatablishment import(
    EstablishmentSerializer,
    EstablishmentRetrieveSerializer
)
from api.models import Establishment


class EstablishmentReadonlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EstablishmentRetrieveSerializer

        return super().get_serializer_class()

