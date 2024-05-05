from rest_framework import serializers

from api.models import Establishment
from api.serializers.consultant import ConsultantSerializer


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = "__all__"


class EstablishmentRetrieveSerializer(serializers.ModelSerializer):
    consultants = ConsultantSerializer(source='consultant_set', read_only=True, many=True)

    class Meta:
        model = Establishment
        fields = ['consultants']
