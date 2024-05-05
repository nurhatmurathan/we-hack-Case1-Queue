from rest_framework import serializers
from api.models import Consultant


class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ['id', 'name', 'number', 'type']


class LiveResponseSerializer(serializers.Serializer):
    headers = serializers.ListField(
        child=serializers.CharField(),
        help_text="Details about live status such as queue length and waiting time"
    )