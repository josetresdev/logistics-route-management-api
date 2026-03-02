from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from apps.routes.utils.response import ResponseHelper

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get('token')
        user = request.user if request.user.is_authenticated else None

        user_data = None
        if user:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }

        return Response(
            ResponseHelper.ok(
                {
                    "token": token,
                    "user": user_data
                },
                message="Token generado correctamente"
            ),
            status=status.HTTP_200_OK
        )
