from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HandleRequestAPIView(APIView):

    def post(self, request):
        try:
            response = self._handle_request()

            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_request(self):
        command_type = self.request.query_params.get('command')


        command_handlers = {
            'date': self._handle_check_command,
            'live': self._handle_pay_command,
        }