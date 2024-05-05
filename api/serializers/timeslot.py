from rest_framework import serializers
from api.models import TimeSlots


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = "__all__"
