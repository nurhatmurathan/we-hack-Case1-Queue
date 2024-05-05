from django.db.models import OuterRef, Exists
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from api.serializers.client import ClientSerializer
from api.models import *


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='command',
            type=OpenApiTypes.STR,
            required=True,
            description='response : OK!',
            enum=['date', 'live']
        ),
        OpenApiParameter(
            name='slot',
            type=OpenApiTypes.STR,
            required=True,
            description='id of slot',
            default="2"
        )
    ],
    request=ClientSerializer(many=False)
)
class HandleRequestAPIView(APIView):

    def post(self, request, establishment_id):
        try:
            print("Query params: ")
            print(establishment_id)
            print(self.request.query_params.get('slot'))
            print((self.request.query_params.get('command')))

            response = self._handle_request(establishment_id)
            return Response(data={'message': response}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_request(self, establishment_id):
        command_type = str(self.request.query_params.get('command')).lower()
        self._validate_type(command_type)

        slot_id = self.request.query_params.get('slot')
        command_handlers = {
            'date': self._handle_date_command,
            'live': self._handle_live_command,
        }

        handler = command_handlers.get(command_type)
        return handler(establishment_id, slot_id)

    def _handle_date_command(self, establishment_id, slot_id):
        print("In date code")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        consultants = establishment.consultant_set.filter(type='date')

        slot = get_object_or_404(TimeSlots, id=slot_id)
        busy_consultants = Booking.objects.filter(date=now().date(), slot=slot).values_list('consultant_id', flat=True)

        available_consultants = consultants.exclude(id__in=busy_consultants)
        self._validate_busy_consultants(available_consultants)

        client = self._create_client(available_consultants.first().id)
        Booking.objects.create(
            slot=slot,
            client=client,
            consultant=available_consultants.first()
        )

        return "OK!"

    def _handle_live_command(self, establishment_id, slot_id):
        establishment = get_object_or_404(Establishment, id=establishment_id)

        clients_with_processing = Client.objects.filter(
            consultant=OuterRef('pk'),
            status='processing'
        )

        available_consultants = establishment.consultant_set.annotate(
            has_processing=Exists(clients_with_processing)
        ).filter(has_processing=False)

        client = self._create_client(available_consultants.first().id)

        return "OK!"

    def _create_client(self, consultant_id=None):
        data = self.request.data

        data['consultant'] = consultant_id

        serializer = ClientSerializer(data=data, many=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return instance

    def _validate_busy_consultants(self, available_consultants):
        if not available_consultants.exists():
            raise NotFound("No available consultants for the given slot and date.")

    def _validate_type(self, command_type):
        if command_type not in ['date', 'live']:
            raise NotFound("Undefined type of consultant.")
