from rest_framework import serializers
from api.models import Client
from rest_framework import serializers
from api.models import Client, Consultant, Establishment, Booking
from api.serializers.consultant import ConsultantSerializer2


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"



class ClientSerializerIIN(serializers.ModelSerializer):
    consultant_info = ConsultantSerializer2(source='consultant', read_only=True)
    waiting_count = serializers.SerializerMethodField()
    booking_info = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['email', 'iin', 'status', 'consultant_info', 'waiting_count', 'booking_info']

    def get_waiting_count(self, obj):
        if obj.consultant and obj.consultant.type == 'live':
            return Client.objects.filter(consultant=obj.consultant, status='waiting').count()
        return None

    def get_booking_info(self, obj):
        if obj.consultant and obj.consultant.type == 'date':
            booking = Booking.objects.filter(client=obj).first()
            return {
                'date': booking.date,
                'time_slot': booking.slot.slot if booking.slot else None,
                'consultant': booking.consultant.name if booking.consultant else None
            }
        return None
