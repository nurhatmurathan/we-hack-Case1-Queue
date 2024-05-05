from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from api.models import *
from api.serializers.client import ClientListSerializer, ClientUpdateSerializer


@extend_schema(
    responses=ClientListSerializer(many=True)
)
class ConsultantClientsListAPIView(APIView):
    def get(self, request):
        try:
            consultant = get_object_or_404(Consultant, id=1)

            clients = consultant.client_set.filter(date=now().date(), status='waiting')
            serializer = ClientListSerializer(clients, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses=ClientUpdateSerializer(many=False),
    request=ClientUpdateSerializer(many=False)
)
class ConsultantClientsUpdateAPIView(APIView):

    def put(self, request, client_id):
        try:
            client = get_object_or_404(Client, id=client_id)

            serializer = ClientUpdateSerializer(client, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)




