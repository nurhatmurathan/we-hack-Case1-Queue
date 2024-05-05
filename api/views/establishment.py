from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from api.serializers.esatablishment import(
    EstablishmentSerializer,
    EstablishmentRetrieveSerializer,
    ConsultantSerializer
)

from api.models import Establishment


class EstablishmentReadonlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EstablishmentRetrieveSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=['get'], url_path="consultants")
    def get_establishment_consultants_by_types(self, request, pk):
        try:
            consultant_type = str(request.query_params.get('type')).lower()
            self._validate_type(consultant_type)

            instance = self.get_object()
            consultants = instance.consultant_set.filter(type=consultant_type)

            serializer = ConsultantSerializer(consultants, many=True)
            return Response(data={'consultants': serializer.data}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    def _validate_type(self, type):
        if type not in ['date', 'live']:
            raise NotFound("Undefined type of consultant.")

