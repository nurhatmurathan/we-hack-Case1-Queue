from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from api.models import Client, Consultant, Booking, TimeSlots
from api.serializers.consultant import ConsultantEstablishmentSerializer
from api.serializers.esatablishment import EstablishmentSerializer


class BookingInfoSerializer(serializers.Serializer):
    date = serializers.DateField()
    time_slot = serializers.CharField()
    consultant = serializers.CharField()


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'email', 'iin', 'status']


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class ClientSerializerIIN(serializers.ModelSerializer):
    consultant_info = ConsultantEstablishmentSerializer(source='consultant', read_only=True)
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
