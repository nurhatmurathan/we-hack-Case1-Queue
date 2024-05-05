from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from api.models import *


class HandleRequestAPIView(APIView):

    def post(self, request):
        try:
            response = self._handle_request()
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_request(self):
        command_type = str(self.request.query_params.get('command')).lower()
        establishment_id = self.request.query_params.get('establishment_id')
        slot_id = self.request.query_params.get('slot_id')

        command_handlers = {
            'date': self._handle_date_command,
            'live': self._handle_live_command,
        }

        handler = command_handlers.get(command_type, None)
        return handler(establishment_id, slot_id)

    def _handle_date_command(self, establishment_id, slot_id):
        establishment = get_object_or_404(Establishment, id=establishment_id)
        consultants = establishment.consultant_set.all()

        slot = get_object_or_404(TimeSlots, id=slot_id)

        busy_consultants = Booking.objects.filter(date=now().date(), slot=slot).values_list('consultant_id', flat=True)
        available_consultants = consultants.exclude(id__in=busy_consultants)

        self._validate_busy_consultants(available_consultants)

        Booking.objects.create(
            slot=slot,
            consultant=available_consultants.first()
        )

        return "OK!"


    def _handle_live_command(self, establishment_id, slot_id):
        pass

    def _validate_busy_consultants(self, available_consultants):
        if not available_consultants.exists():
            raise NotFound("No available consultants for the given slot and date.")
