from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils.timezone import now


from api.models import Consultant, Client, Establishment, TimeSlots, Booking
from api.serializers.consultant import LiveResponseSerializer
from api.serializers.timeslot import TimeSlotSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='command',
            type=OpenApiTypes.STR,
            required=True,
            description='Command to execute, determines the type of response',
            enum=['date', 'live']
        )
    ],
    responses={
        200: inline_serializer(
            name='CommandResponse',
            fields={
                'date': TimeSlotSerializer(help_text="Response if 'date' command is issued"),
                'live': LiveResponseSerializer(help_text="Response if 'live' command is issued"),
            },
            many=False,
        )
    }
)
class RecordAPIView(APIView):

    def get(self, request, establishment_id):
        try:
            response = self._handle_request(request, establishment_id)

            if response is None:
                return Response(data={'error': 'Invalid command type'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _handle_request(self, request, establishment_id):
        command_type = str(request.query_params.get('command', '')).lower()

        command_handlers = {
            'date': self._handle_date_command,
            'live': self._handle_live_command,
        }

        handler = command_handlers.get(command_type, None)
        if handler is not None:
            return handler(establishment_id)
        else:
            raise KeyError("Command handler not found for the provided command type.")

    def _handle_date_command(self, establishment_id):
        establishment = get_object_or_404(Establishment, id=establishment_id)
        consultants = establishment.consultant_set.filter(type='date')

        all_slots = TimeSlots.objects.all()
        bookings = Booking.objects.filter(
            date=now().date(),
            consultant__in=consultants
        ).values('slot_id').annotate(booked_count=Count('slot_id'))
        bookings_map = {booking['slot_id']: booking['booked_count'] for booking in bookings}

        available_slots = []
        for slot in all_slots:
            booked_count = bookings_map.get(slot.id, 0)
            if booked_count < consultants.count():
                available_slots.append(slot)

        serializer = TimeSlotSerializer(available_slots, many=True)
        return {'result': serializer.data}

    def _handle_live_command(self, establishment_id):
        consultants = Consultant.objects.filter(establishment_id=establishment_id)
        clients = Client.objects.filter(consultant__in=consultants, status__in=['processing', 'waiting'])
        clients_in_processing = clients.filter(status="processing")

        return {'headers': [
            f"Свободные окошки {len(consultants)}/{len(consultants) - len(clients_in_processing)}",
            f"В очереди {len(clients)} человек",
            f"Время ожидания {(len(clients) - len(clients_in_processing)) * 15} мин"
        ]}


