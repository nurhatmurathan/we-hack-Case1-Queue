from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from api.models import Client, Consultant, Establishment, Booking, TimeSlots


class BookingInfoSerializer(serializers.Serializer):
    date = serializers.DateField()
    time_slot = serializers.CharField()
    consultant = serializers.CharField()


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ['id', 'name', 'address', 'url']


class ConsultantSerializer(serializers.ModelSerializer):
    establishment = EstablishmentSerializer()

    class Meta:
        model = Consultant
        fields = ['id', 'name', 'type', 'establishment']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = ['slot']


class ClientSerializerIIN(serializers.ModelSerializer):
    consultant_info = ConsultantSerializer(source='consultant', read_only=True)
    waiting_count = serializers.IntegerField(read_only=True, required=False)
    booking_info = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['email', 'iin', 'status', 'consultant_info', 'waiting_count', 'booking_info']

    @extend_schema_field(BookingInfoSerializer(many=False))
    def get_booking_info(self, obj):
        if obj.consultant and obj.consultant.type == 'date':
            booking = Booking.objects.filter(client=obj).first()
            if booking:
                return {
                    'date': booking.date,
                    'time_slot': booking.slot.slot if booking.slot else None,
                    'consultant': booking.consultant.name if booking.consultant else None
                }
        return None
