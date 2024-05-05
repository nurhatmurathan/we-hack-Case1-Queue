from rest_framework import serializers
from api.models import Consultant


class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ['id', 'name', 'number', 'type']
